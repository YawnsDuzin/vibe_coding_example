# /create-form

폼 사양을 PyQt5 위젯 클래스로 변환하는 Skill입니다.

## 용도
폼 이름과 필드 목록을 입력하면 보일러플레이트 패턴에 맞는 PyQt5 폼 위젯을 생성합니다.

## 실행 내용

1. **폼 위젯 클래스 생성**: `app/ui/<이름>_form.py`
   - login_form.py와 동일한 구조
   - QVBoxLayout 기반 레이아웃
   - 각 필드에 적절한 위젯 (QLineEdit, QComboBox, QCheckBox 등)
   - 입력 검증 로직
   - 시그널/슬롯 연결
2. **Service 연결 스캐폴딩**: Service 호출 코드 포함
3. **main_window.py 등록 안내**: 새 페이지 추가 방법

## 입력 예시
```
폼명: task_form
필드: 제목(QLineEdit,필수), 설명(QLineEdit), 우선순위(QComboBox:높음/중간/낮음), 마감일(QLineEdit,YYYY-MM-DD)
```

## 사용되는 단원
- 단원 5: PyQt5 UI
- 캡스톤 프로젝트
