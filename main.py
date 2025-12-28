import time  # 시간 측정용
from pathlib import Path  # 파일 경로 처리용
from detector import OneShotDetector  # 아이콘 감지기
from timer_overlay import TimerOverlay  # 타이머 UI
from region_selector import RegionSelector, RegionIndicator  # 영역 선택기 + 표시기
from config import load_config, save_config  # 설정 관리

class OneShotTimerApp:
    """일격필살 타이머 메인 앱"""
    
    def __init__(self):
        """앱 초기화"""
        # 설정 불러오기
        self.config = load_config()
        
        # 아이콘 이미지 경로
        icon_path = Path("assets/oneshot_icon.png")
        
        # 아이콘 파일 존재 확인
        if not icon_path.exists():
            print("=" * 50)
            print("⚠️ assets/oneshot_icon.png 파일이 필요합니다!")
            print("   일격필살 버프 아이콘을 캡처해서 저장해주세요.")
            print("=" * 50)
        
        # ========== 컴포넌트 초기화 ==========
        self.detector = OneShotDetector(
            str(icon_path),
            threshold=self.config["detection_threshold"]
        )
        
        self.overlay = TimerOverlay()
        
        # 영역 표시기 (희미한 테두리)
        self.region_indicator = RegionIndicator(self.overlay.root)
        
        # 영역 선택기 (현재 열려있는 것 추적)
        self.current_selector = None
        
        # ========== 상태 변수 ==========
        self.is_active = False
        self.timer_running = False
        self.timer_start_time = 0.0
        self.cooldown = self.config["cooldown"]
        self.last_detected = False
        
        # ========== 감지 쿨다운 (중복 감지 방지) ==========
        self.detection_cooldown = 10.0
        self.last_trigger_time = 0.0
        
        # ========== 감지 영역 설정 ==========
        if self.config["detection_region"]:
            r = self.config["detection_region"]
            self.detector.set_region(r["x"], r["y"], r["width"], r["height"])
            self.region_indicator.show(r["x"], r["y"], r["width"], r["height"])
        
        # ========== 오버레이 위치 복원 ==========
        pos = self.config["overlay_position"]
        self.overlay.set_position(pos["x"], pos["y"])
        
        # ========== 버튼 콜백 연결 ==========
        self.overlay.on_start = self.start_detection
        self.overlay.on_stop = self.stop_detection
        self.overlay.on_region = self.open_region_selector
        self.overlay.on_quit = self.quit_app
        
        # 초기 상태 표시
        if self.config["detection_region"]:
            self.overlay.set_status("영역 설정됨")
        else:
            self.overlay.set_status("영역 버튼을 눌러 감지 영역을 설정하세요")
    
    def start_detection(self):
        """시작 버튼 클릭 - 감지 시작"""
        # 영역 선택기가 열려있으면 자동으로 확인 처리
        if self.current_selector is not None:
            try:
                self.current_selector._on_confirm()
            except:
                pass
            self.current_selector = None
        
        # 영역이 설정 안 됐으면 경고
        if not self.config["detection_region"]:
            self.overlay.set_status("먼저 영역을 설정하세요!")
            return
        
        self.is_active = True
        self.last_trigger_time = 0.0
        self.overlay.set_running(True)
        self.overlay.set_status("감지 중...")
        self._detection_loop()
    
    def stop_detection(self):
        """정지 버튼 클릭 - 감지 중지"""
        self.is_active = False
        self.timer_running = False
        self.overlay.set_running(False)
        self.overlay.update_timer(0)
        self.overlay.set_status("정지됨")
        self._save_position()
    
    def open_region_selector(self):
        """영역 설정 버튼 클릭 - 영역 선택기 열기"""
        # 이미 열려있으면 닫기
        if self.current_selector is not None:
            try:
                self.current_selector.root.destroy()
            except:
                pass
            self.current_selector = None
        
        # 감지 중이면 먼저 정지
        self.is_active = False
        self.timer_running = False
        
        # 영역 표시기 숨기기
        self.region_indicator.hide()
        
        # 영역 선택기 생성
        selector = RegionSelector()
        self.current_selector = selector  # 추적용 저장
        
        # 기존 영역이 있으면 그 위치로 초기화
        if self.config["detection_region"]:
            r = self.config["detection_region"]
            selector.set_region(r["x"], r["y"], r["width"], r["height"])
        
        # 확인 버튼 콜백 연결
        selector.on_confirm = self._on_region_confirmed
        
        self.overlay.set_status("영역을 설정하고 확인을 누르세요")
    
    def _on_region_confirmed(self, region: dict):
        """영역 선택 완료 콜백"""
        # 선택기 추적 해제
        self.current_selector = None
        
        # 설정에 저장
        self.config["detection_region"] = region
        save_config(self.config)
        
        # 감지기에 영역 적용
        self.detector.set_region(
            region["x"],
            region["y"],
            region["width"],
            region["height"]
        )
        
        # 영역 표시기 업데이트
        self.region_indicator.show(
            region["x"],
            region["y"],
            region["width"],
            region["height"]
        )
        
        self.overlay.set_status("영역 설정 완료!")
    
    def quit_app(self):
        """종료 버튼 클릭 - 앱 종료"""
        # 먼저 위치 저장
        try:
            x, y = self.overlay.get_position()
            self.config["overlay_position"] = {"x": x, "y": y}
            save_config(self.config)
        except:
            pass
        
        self.is_active = False
        self.region_indicator.hide()
        
        # 영역 선택기 열려있으면 닫기
        if self.current_selector is not None:
            try:
                self.current_selector.root.destroy()
            except:
                pass
        
        try:
            self.region_indicator.window.destroy()
        except:
            pass
    
    def _detection_loop(self):
        """메인 감지 루프"""
        if not self.is_active:
            return
        
        current_time = time.time()
        
        # ========== 감지 쿨다운 체크 ==========
        time_since_trigger = current_time - self.last_trigger_time
        can_detect = time_since_trigger >= self.detection_cooldown
        
        if can_detect:
            detected = self.detector.detect()
            
            match_val = self.detector.get_last_match_value()
            threshold = self.detector.threshold
            
            if detected:
                self._start_timer()
                self.last_trigger_time = current_time
            else:
                if not self.timer_running:
                    self.overlay.set_status(f"매칭: {match_val:.2f} / 기준: {threshold:.2f}")
        else:
            remaining_cooldown = self.detection_cooldown - time_since_trigger
            if not self.timer_running:
                self.overlay.set_status(f"재감지 대기: {remaining_cooldown:.1f}초")
        
        # ========== 타이머 업데이트 ==========
        if self.timer_running:
            elapsed = current_time - self.timer_start_time
            remaining = self.cooldown - elapsed
            
            if remaining <= 0:
                self.timer_running = False
                self.overlay.update_timer(0)
                self.overlay.set_status("준비 완료!")
            else:
                self.overlay.update_timer(remaining)
        
        self.overlay.schedule(
            self.config["scan_interval_ms"],
            self._detection_loop
        )
    
    def _start_timer(self):
        """일격필살 감지됨 - 타이머 시작"""
        self.timer_running = True
        self.timer_start_time = time.time()
        self.overlay.set_status("일격필살 발동!")
    
    def _save_position(self):
        """오버레이 창 위치 저장"""
        try:
            x, y = self.overlay.get_position()
            self.config["overlay_position"] = {"x": x, "y": y}
            save_config(self.config)
        except:
            pass
    
    def run(self):
        """앱 실행"""
        print("=" * 50)
        print("일격필살 타이머")
        print("=" * 50)
        print(f"쿨타임: {self.cooldown:.0f}초")
        print(f"감지 쿨다운: {self.detection_cooldown:.0f}초")
        print("1. [영역] 버튼으로 감지 영역 설정")
        print("2. [시작] 버튼으로 감지 시작")
        print("=" * 50)
        
        try:
            self.overlay.run()
        except:
            pass


# ========== 프로그램 시작점 ==========
if __name__ == "__main__":
    app = OneShotTimerApp()
    app.run()