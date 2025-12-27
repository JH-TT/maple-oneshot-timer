import tkinter as tk  # Python 기본 GUI 라이브러리
from typing import Callable, Optional  # 타입 힌트용

class TimerOverlay:
    """화면에 표시되는 타이머 오버레이 창"""
    
    def __init__(self):
        """타이머 오버레이 초기화"""
        
        # ========== 메인 윈도우 설정 ==========
        self.root = tk.Tk()
        self.root.title("일격필살 타이머")
        
        # 창 속성 설정
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)
        self.root.overrideredirect(True)
        
        # ========== 메인 프레임 ==========
        self.frame = tk.Frame(
            self.root,
            bg="#1a1a2e",
            padx=10,
            pady=8
        )
        self.frame.pack()
        
        # ========== 타이머 숫자 라벨 ==========
        self.timer_label = tk.Label(
            self.frame,
            text="대기중",
            font=("맑은 고딕", 24, "bold"),
            fg="#00ff88",
            bg="#1a1a2e",
            width=8
        )
        self.timer_label.pack()
        
        # ========== 상태 텍스트 라벨 ==========
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("맑은 고딕", 10),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.status_label.pack()
        
        # ========== 버튼 프레임 ==========
        self.btn_frame = tk.Frame(self.frame, bg="#1a1a2e")
        self.btn_frame.pack(pady=(8, 0))
        
        # 시작 버튼 (초록색)
        self.start_btn = tk.Button(
            self.btn_frame,
            text="시작",
            command=self._on_start,
            bg="#4CAF50",
            fg="white",
            width=6
        )
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        # 정지 버튼 (빨간색) - 처음엔 비활성화
        self.stop_btn = tk.Button(
            self.btn_frame,
            text="정지",
            command=self._on_stop,
            bg="#f44336",
            fg="white",
            width=6,
            state=tk.DISABLED  # 비활성화 상태로 시작
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # 영역 설정 버튼 (파란색)
        self.region_btn = tk.Button(
            self.btn_frame,
            text="영역",
            command=self._on_region,
            bg="#2196F3",
            fg="white",
            width=6
        )
        self.region_btn.pack(side=tk.LEFT, padx=2)
        
        # 종료 버튼 (회색)
        self.quit_btn = tk.Button(
            self.btn_frame,
            text="종료",
            command=self._on_quit,
            bg="#666666",
            fg="white",
            width=6
        )
        self.quit_btn.pack(side=tk.LEFT, padx=2)
        
        # ========== 드래그 기능 설정 ==========
        self._drag_data = {"x": 0, "y": 0}
        
        self.frame.bind("<Button-1>", self._on_drag_start)
        self.frame.bind("<B1-Motion>", self._on_drag_motion)
        self.timer_label.bind("<Button-1>", self._on_drag_start)
        self.timer_label.bind("<B1-Motion>", self._on_drag_motion)
        
        # ========== 콜백 함수 저장용 ==========
        self.on_start: Optional[Callable] = None
        self.on_stop: Optional[Callable] = None
        self.on_region: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None
        
        # ========== 타이머 상태 ==========
        self.remaining_time = 0.0
        self.is_running = False
    
    # ========== 드래그 관련 함수 ==========
    
    def _on_drag_start(self, event):
        """드래그 시작"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    
    def _on_drag_motion(self, event):
        """드래그 중 - 창 이동"""
        x = self.root.winfo_x() + event.x - self._drag_data["x"]
        y = self.root.winfo_y() + event.y - self._drag_data["y"]
        self.root.geometry(f"+{x}+{y}")
    
    # ========== 버튼 클릭 핸들러 ==========
    
    def _on_start(self):
        """시작 버튼 클릭됨"""
        if self.on_start:
            self.on_start()
    
    def _on_stop(self):
        """정지 버튼 클릭됨"""
        if self.on_stop:
            self.on_stop()
    
    def _on_region(self):
        """영역 설정 버튼 클릭됨"""
        if self.on_region:
            self.on_region()
    
    def _on_quit(self):
        """종료 버튼 클릭됨"""
        if self.on_quit:
            self.on_quit()
        self.root.quit()
    
    # ========== 버튼 상태 제어 ==========
    
    def set_running(self, is_running: bool):
        """
        감지 상태에 따라 버튼 활성화/비활성화
        
        Args:
            is_running: True면 감지 중, False면 정지 상태
        """
        if is_running:
            # 감지 중: 시작 비활성화, 정지 활성화
            self.start_btn.config(state=tk.DISABLED, bg="#2E7D32")  # 어두운 초록
            self.stop_btn.config(state=tk.NORMAL, bg="#f44336")
            self.region_btn.config(state=tk.DISABLED, bg="#1565C0")  # 어두운 파랑
        else:
            # 정지 상태: 시작 활성화, 정지 비활성화
            self.start_btn.config(state=tk.NORMAL, bg="#4CAF50")
            self.stop_btn.config(state=tk.DISABLED, bg="#8B0000")  # 어두운 빨강
            self.region_btn.config(state=tk.NORMAL, bg="#2196F3")
    
    # ========== 외부에서 호출하는 함수들 ==========
    
    def update_timer(self, seconds: float):
        """타이머 표시 업데이트"""
        self.remaining_time = seconds
        
        if seconds <= 0:
            self.timer_label.config(text="준비!", fg="#00ff88")
        elif seconds <= 5:
            self.timer_label.config(text=f"{seconds:.1f}초", fg="#ff6b6b")
        else:
            self.timer_label.config(text=f"{seconds:.1f}초", fg="#ffd93d")
    
    def set_status(self, text: str):
        """상태 텍스트 업데이트"""
        self.status_label.config(text=text)
    
    def set_position(self, x: int, y: int):
        """오버레이 창 위치 설정"""
        self.root.geometry(f"+{x}+{y}")
    
    def get_position(self) -> tuple:
        """현재 오버레이 창 위치 반환"""
        return (self.root.winfo_x(), self.root.winfo_y())
    
    def run(self):
        """오버레이 창 실행"""
        self.root.mainloop()
    
    def schedule(self, ms: int, callback: Callable):
        """일정 시간 후 함수 실행 예약"""
        self.root.after(ms, callback)