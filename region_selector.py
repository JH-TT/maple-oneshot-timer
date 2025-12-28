import tkinter as tk  # GUI 라이브러리
from typing import Callable, Optional  # 타입 힌트용

class RegionSelector:
    """마우스로 감지 영역을 설정하는 투명 박스"""
    
    def __init__(self):
        """영역 선택기 초기화"""
        
        # ========== 화면 크기 가져오기 ==========
        self.root = tk.Toplevel()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # ========== 메인 윈도우 ==========
        self.root.title("영역 설정")
        
        # 창 속성
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)
        self.root.overrideredirect(True)
        
        # 초기 크기와 위치
        self.width = 300
        self.height = 100
        self.x = 100
        self.y = 100
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        
        # ========== 메인 프레임 ==========
        self.frame = tk.Frame(
            self.root,
            bg="#00ff00",
            highlightbackground="#ffffff",
            highlightthickness=3
        )
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== 안내 라벨 ==========
        self.label = tk.Label(
            self.frame,
            text="드래그: 이동\n모서리: 크기 조절",
            font=("맑은 고딕", 10),
            fg="white",
            bg="#00ff00"
        )
        self.label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # ========== 확인 버튼 ==========
        self.confirm_btn = tk.Button(
            self.frame,
            text="확인",
            command=self._on_confirm,
            bg="#4CAF50",
            fg="white",
            width=8
        )
        self.confirm_btn.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        # ========== 크기 조절 핸들 (오른쪽 아래) ==========
        self.resize_handle_br = tk.Frame(
            self.frame,
            bg="#ffffff",
            width=15,
            height=15,
            cursor="bottom_right_corner"
        )
        self.resize_handle_br.place(relx=1.0, rely=1.0, anchor=tk.SE)
        
        # ========== 크기 조절 핸들 (왼쪽 아래) ==========
        self.resize_handle_bl = tk.Frame(
            self.frame,
            bg="#ffffff",
            width=15,
            height=15,
            cursor="bottom_left_corner"
        )
        self.resize_handle_bl.place(relx=0.0, rely=1.0, anchor=tk.SW)
        
        # ========== 드래그 데이터 ==========
        self._drag_data = {"x": 0, "y": 0}
        self._resize_data = {"x": 0, "y": 0, "width": 0, "height": 0, "orig_x": 0}
        
        # ========== 이벤트 바인딩 ==========
        self.frame.bind("<Button-1>", self._on_drag_start)
        self.frame.bind("<B1-Motion>", self._on_drag_motion)
        self.label.bind("<Button-1>", self._on_drag_start)
        self.label.bind("<B1-Motion>", self._on_drag_motion)
        
        # 오른쪽 아래 핸들
        self.resize_handle_br.bind("<Button-1>", self._on_resize_br_start)
        self.resize_handle_br.bind("<B1-Motion>", self._on_resize_br_motion)
        
        # 왼쪽 아래 핸들
        self.resize_handle_bl.bind("<Button-1>", self._on_resize_bl_start)
        self.resize_handle_bl.bind("<B1-Motion>", self._on_resize_bl_motion)
        
        # ========== 콜백 ==========
        self.on_confirm: Optional[Callable[[dict], None]] = None
    
    def _clamp_position(self):
        """영역이 화면 밖으로 나가지 않도록 제한"""
        # X 좌표 제한
        if self.x < 0:
            self.x = 0
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width
        
        # Y 좌표 제한
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height
    
    def _on_drag_start(self, event):
        """드래그 시작"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    
    def _on_drag_motion(self, event):
        """드래그 중 - 창 이동"""
        self.x = self.root.winfo_x() + event.x - self._drag_data["x"]
        self.y = self.root.winfo_y() + event.y - self._drag_data["y"]
        self._clamp_position()
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
    
    # ========== 오른쪽 아래 핸들 ==========
    
    def _on_resize_br_start(self, event):
        """오른쪽 아래 크기 조절 시작"""
        self._resize_data["x"] = event.x_root
        self._resize_data["y"] = event.y_root
        self._resize_data["width"] = self.width
        self._resize_data["height"] = self.height
    
    def _on_resize_br_motion(self, event):
        """오른쪽 아래 크기 조절 중"""
        dx = event.x_root - self._resize_data["x"]
        dy = event.y_root - self._resize_data["y"]
        
        new_width = max(50, self._resize_data["width"] + dx)
        new_height = max(50, self._resize_data["height"] + dy)
        
        # 화면 밖으로 나가지 않도록
        if self.x + new_width > self.screen_width:
            new_width = self.screen_width - self.x
        if self.y + new_height > self.screen_height:
            new_height = self.screen_height - self.y
        
        self.width = new_width
        self.height = new_height
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
    
    # ========== 왼쪽 아래 핸들 ==========
    
    def _on_resize_bl_start(self, event):
        """왼쪽 아래 크기 조절 시작"""
        self._resize_data["x"] = event.x_root
        self._resize_data["y"] = event.y_root
        self._resize_data["width"] = self.width
        self._resize_data["height"] = self.height
        self._resize_data["orig_x"] = self.x
    
    def _on_resize_bl_motion(self, event):
        """왼쪽 아래 크기 조절 중"""
        dx = event.x_root - self._resize_data["x"]
        dy = event.y_root - self._resize_data["y"]
        
        # 왼쪽 아래는 X가 반대로
        new_width = max(50, self._resize_data["width"] - dx)
        new_height = max(50, self._resize_data["height"] + dy)
        new_x = self._resize_data["orig_x"] + dx
        
        # 화면 밖으로 나가지 않도록
        if new_x < 0:
            new_width = self._resize_data["width"] + self._resize_data["orig_x"]
            new_x = 0
        if self.y + new_height > self.screen_height:
            new_height = self.screen_height - self.y
        
        self.x = new_x
        self.width = new_width
        self.height = new_height
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
    
    def _on_confirm(self):
        """확인 버튼 클릭"""
        region = {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }
        
        if self.on_confirm:
            self.on_confirm(region)
        
        self.root.destroy()
    
    def set_region(self, x: int, y: int, width: int, height: int):
        """기존 영역으로 초기화"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._clamp_position()
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
    
    def show(self):
        """영역 선택기 표시"""
        self.root.deiconify()


class RegionIndicator:
    """설정된 영역을 희미하게 표시하는 테두리"""
    
    def __init__(self, root):
        """영역 표시기 초기화"""
        self.window = tk.Toplevel(root)
        self.window.title("")
        
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.3)
        self.window.overrideredirect(True)
        
        self.frame = tk.Frame(
            self.window,
            bg="",
            highlightbackground="#00ff00",
            highlightthickness=2
        )
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.window.wm_attributes("-transparentcolor", "gray")
        self.frame.config(bg="gray")
        
        self.window.withdraw()
    
    def show(self, x: int, y: int, width: int, height: int):
        """영역 표시"""
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.deiconify()
    
    def hide(self):
        """영역 숨기기"""
        self.window.withdraw()
    
    def update_position(self, x: int, y: int, width: int, height: int):
        """영역 위치/크기 업데이트"""
        self.window.geometry(f"{width}x{height}+{x}+{y}")