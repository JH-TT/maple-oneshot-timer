import json  # JSON 파일 처리용
from pathlib import Path  # 파일 경로 처리용

# 설정 파일 경로
CONFIG_FILE = Path("config.json")

# 기본 설정값
DEFAULT_CONFIG = {
    "cooldown": 30.0,  # 쿨타임 30초 고정
    "detection_region": None,  # 감지할 화면 영역
    "overlay_position": {"x": 100, "y": 100},  # 타이머 창 위치
    "detection_threshold": 0.8,  # 이미지 매칭 정확도 (80%)
    "scan_interval_ms": 100,  # 화면 스캔 주기 (0.1초)
}

def load_config():
    """설정 파일 불러오기"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
            return {**DEFAULT_CONFIG, **saved}
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """설정 파일 저장하기"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)