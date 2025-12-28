# 🎮 메이플스토리 일격필살 타이머

메이플스토리 5차 특수스킬 **일격필살**의 쿨타임을 추적하는 오버레이 타이머입니다.

일격필살은 쿨타임이 화면에 표시되지 않아 타이밍 맞추기가 어려운데, 이 프로그램이 버프 아이콘을 감지해서 자동으로 30초 타이머를 시작합니다.

---

## ✨ 기능

- 🔍 일격필살 버프 아이콘 자동 감지
- ⏱️ 30초 쿨타임 타이머 표시
- 🖱️ 드래그로 타이머 위치 이동
- 📐 감지 영역 직접 설정 가능
- 💾 설정 자동 저장

---

## 📥 다운로드

[Releases](../../releases) 페이지에서 최신 버전을 다운로드하세요.

---

## 🚀 사용 방법

### 1. 아이콘 이미지 준비

1. 메이플스토리에서 일격필살 발동
2. 버프창에 아이콘이 나타날 때 `Win + Shift + S`로 캡처
3. `assets/oneshot_icon.png`로 저장

### 2. 프로그램 실행

1. `OneShotTimer.exe` 실행
2. **영역** 버튼 클릭 → 버프창 위치로 초록색 박스 이동 → **확인**
3. **시작** 버튼 클릭 → 감지 시작!

### 3. 버튼 설명

| 버튼 | 기능 |
|------|------|
| 시작 | 아이콘 감지 시작 |
| 정지 | 감지 중지 |
| 영역 | 감지할 화면 영역 설정 |
| 종료 | 프로그램 종료 |

---

## 📁 폴더 구조
```
OneShotTimer/
├── OneShotTimer.exe
└── assets/
    └── oneshot_icon.png   ← 직접 캡처 필요
```

---

## ⚙️ 설정 (config.json)

| 항목 | 기본값 | 설명 |
|------|--------|------|
| cooldown | 30.0 | 쿨타임 (초) |
| detection_threshold | 0.5 | 매칭 정확도 기준 (0.0~1.0) |
| scan_interval_ms | 100 | 화면 스캔 주기 (ms) |

---

## 🛠️ 직접 빌드하기

### 요구사항

- Python 3.10 이상
- pip 패키지: opencv-python, mss, numpy, Pillow, pyinstaller

### 빌드 방법
```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
pip install pyinstaller

# exe 빌드
pyinstaller --onefile --noconsole --name "OneShotTimer" main.py
```

빌드된 파일: `dist/OneShotTimer.exe`

---

## ⚠️ 주의사항

- 게임 해상도에 맞는 아이콘을 직접 캡처해야 합니다
- 감지가 잘 안 되면 `config.json`에서 `detection_threshold` 값을 낮춰보세요
- 본 프로그램은 화면 캡처만 사용하며, 게임 메모리를 조작하지 않습니다

---

## 📝 라이선스

MIT License
```

`Ctrl + S`로 저장

---

## GitHub Releases로 exe 배포하기

### 방법 1: 웹에서 직접 올리기

1. GitHub 저장소 페이지 접속
2. 오른쪽 **Releases** 클릭
3. **Create a new release** 클릭
4. Tag: `v1.0.0-beta`
5. Title: `v1.0.0-beta 일격필살 타이머`
6. 설명 작성
7. **Attach binaries** 영역에 `OneShotTimer.zip` 드래그해서 업로드
8. **Publish release** 클릭

---

### ZIP 파일 준비
```
OneShotTimer.zip (이 안에)
├── OneShotTimer.exe
└── assets/
    └── (빈 폴더 또는 샘플 이미지)