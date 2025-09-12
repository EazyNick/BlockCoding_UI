# 블록 코딩 UI - 자동화 도구

![프로그램 스크린샷](https://github.com/EazyNick/BlockCoding_UI/assets/123717093/19d3494a-9b0d-4c55-807b-8af6d90e40a2)

## 프로그램 소개

이 프로그램은 PyQt5를 기반으로 한 **노드 기반 자동화 도구**입니다. 사용자가 드래그 앤 드롭으로 다양한 기능 블록들을 배치하고, 순차적으로 실행하여 마우스 클릭, 스크롤 등의 자동화 작업을 수행할 수 있습니다.

### 주요 기능

- **노드 기반 인터페이스**: 시각적으로 직관적인 블록 코딩 방식
- **마우스 자동화**: 지정된 좌표에서 마우스 클릭 실행
- **스크롤 자동화**: 드래그 앤 드롭 스크롤 기능
- **명령어 실행**: 시스템 명령어 실행 기능
- **실시간 실행**: 노드들을 순차적으로 실행하여 자동화 작업 수행
- **프로젝트 저장/불러오기**: 작업한 노드 구성을 JSON 파일로 저장 및 불러오기
- **멀티스레딩**: 백그라운드에서 안전하게 자동화 작업 실행

### 지원하는 노드 타입

1. **Click Node**: 지정된 좌표에서 마우스 클릭
2. **Scroll Node**: 마우스 드래그를 통한 스크롤
3. **Command Node**: 시스템 명령어 실행

## 설치 방법

### 1. 시스템 요구사항

- **운영체제**: Windows 10/11
- **Python**: 3.7 이상
- **메모리**: 최소 4GB RAM 권장

### 2. Python 설치

1. [Python 공식 웹사이트](https://www.python.org/downloads/)에서 Python 3.7 이상 버전을 다운로드
2. 설치 시 "Add Python to PATH" 옵션을 체크하여 환경변수에 추가
3. 설치 완료 후 명령 프롬프트에서 `python --version`으로 설치 확인

### 3. 프로젝트 다운로드

```bash
git clone https://github.com/EazyNick/BlockCoding_UI.git
cd BlockCoding_UI
```

### 4. 필요한 패키지 설치

```bash
pip install PyQt5
pip install pyautogui
```

또는 requirements.txt 파일이 있다면:

```bash
pip install -r requirements.txt
```

### 5. 프로그램 실행

```bash
python main.py
```

## 사용 방법

1. **노드 추가**: 왼쪽 패널의 "Add Click" 버튼을 클릭하여 클릭 노드 추가
2. **좌표 설정**: 노드 하단의 입력창에 "x, y, delay" 형식으로 좌표와 지연시간 입력
3. **노드 배치**: 노드를 원하는 위치로 드래그하여 배치
4. **실행**: "실행" 버튼을 클릭하여 노드들을 순차적으로 실행
5. **저장/불러오기**: 작업한 노드 구성을 저장하거나 이전에 저장한 구성을 불러오기

## 프로젝트 구조

```
BlockCoding_UI/
├── main.py                 # 메인 실행 파일
├── GUI.py                  # 메인 GUI 클래스
├── node.py                 # 노드 클래스 정의
├── define.py               # 공통 함수 정의
├── Execute_Def/            # 실행 함수들
│   ├── Click.py           # 마우스 클릭 함수
│   ├── Scroll.py          # 스크롤 함수
│   └── Command.py         # 명령어 실행 함수
├── Override_Custom/        # 커스텀 UI 컴포넌트
├── Thread/                 # 멀티스레딩 관련
├── Logger/                 # 로깅 시스템
├── SaveAction/            # 저장/불러오기 기능
└── Data/                  # 데이터 저장 폴더
```

## 주의사항

- 이 프로그램은 자동화 도구이므로 사용 시 주의가 필요합니다
- 마우스 클릭이 실행되는 동안 다른 작업을 하지 마세요
- 실행 중 문제가 발생하면 "중단" 버튼을 눌러 작업을 중지할 수 있습니다

## 개발자 정보

- **개발자**: EazyNick
- **이메일**: kkkygsos@naver.com
- **GitHub**: [EazyNick](https://github.com/EazyNick)

## 라이선스

MIT License

---

[View English README.md](readme/README_original.md)
