import cv2          # 이미지 처리 라이브러리
import numpy as np  # 숫자/배열 처리 라이브러리
import mss          # 초고속 화면 캡처 라이브러리

class OneShotDetector:
    """일격필살 버프 아이콘을 화면에서 감지하는 클래스"""
    
    def __init__(self, icon_path: str, threshold: float = 0.8):
        """
        감지기 초기화
        
        Args:
            icon_path: 일격필살 아이콘 이미지 파일 경로
            threshold: 매칭 정확도 기준 (0.0~1.0, 높을수록 엄격)
        """
        # 아이콘 이미지 파일 읽기
        self.template_original = cv2.imread(icon_path, cv2.IMREAD_COLOR)
        
        # 파일이 없으면 에러 발생
        if self.template_original is None:
            raise FileNotFoundError(f"아이콘 이미지를 찾을 수 없습니다: {icon_path}")
        
        # 그레이스케일로 변환
        self.template_original = cv2.cvtColor(self.template_original, cv2.COLOR_BGR2GRAY)
        
        # 매칭 정확도 기준값 저장
        self.threshold = threshold
        
        # 화면 캡처 도구 초기화
        self.sct = mss.mss()
        
        # 감지할 화면 영역
        self.detection_region = None
        
        # 디버그 모드
        self.debug = True
        self.last_max_val = 0.0
        
        # 멀티스케일: 검색할 크기 비율들 (50% ~ 150%)
        self.scales = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    
    def set_region(self, x: int, y: int, width: int, height: int):
        """감지할 화면 영역 설정"""
        self.detection_region = {
            "left": x,
            "top": y,
            "width": width,
            "height": height
        }
    
    def detect(self) -> bool:
        """
        화면에서 일격필살 아이콘이 있는지 감지 (멀티스케일)
        
        Returns:
            True: 아이콘 발견됨
            False: 아이콘 없음
        """
        # 감지 영역 결정
        if self.detection_region is None:
            monitor = self.sct.monitors[1]
            region = monitor
        else:
            region = self.detection_region
        
        # 화면 캡처
        screenshot = self.sct.grab(region)
        
        # numpy 배열로 변환
        frame = np.array(screenshot)
        
        # 그레이스케일로 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        
        # 여러 크기로 매칭 시도
        best_val = 0.0
        best_scale = 1.0
        
        for scale in self.scales:
            # 템플릿 크기 조절
            width = int(self.template_original.shape[1] * scale)
            height = int(self.template_original.shape[0] * scale)
            
            # 너무 작거나 화면보다 크면 스킵
            if width < 10 or height < 10:
                continue
            if width > frame.shape[1] or height > frame.shape[0]:
                continue
            
            # 크기 조절
            template = cv2.resize(self.template_original, (width, height))
            
            # 템플릿 매칭 수행
            result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            
            # 최대값 찾기
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            # 가장 높은 값 저장
            if max_val > best_val:
                best_val = max_val
                best_scale = scale
        
        # 디버그: 매칭 값 저장 및 출력
        self.last_max_val = best_val
        if self.debug:
            print(f"매칭 값: {best_val:.3f} / 기준: {self.threshold:.3f} / 스케일: {best_scale:.1f}")
        
        # 정확도가 기준값 이상이면 아이콘 발견
        return best_val >= self.threshold
    
    def set_threshold(self, threshold: float):
        """임계값 변경"""
        self.threshold = threshold
    
    def get_last_match_value(self) -> float:
        """마지막 매칭 값 반환"""
        return self.last_max_val