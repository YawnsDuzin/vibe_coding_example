# CLAUDE.md — 바이브코딩 교육용 보일러플레이트

이 파일은 Claude Code가 이 프로젝트에서 작업할 때 참고하는 가이드입니다.

## 프로젝트 개요
비개발자(기획자, PM, 디자이너, 현업 실무자)를 위한 **PyQt5 데스크톱 앱 보일러플레이트**입니다.
이 프로젝트를 기반으로 자신만의 업무 도구를 만들어 나갑니다.

## 기술 스택 (변경 불가)
- **언어**: Python
- **GUI**: PyQt5 + Qt Designer
- **DB**: SQLite (기본) → PostgreSQL (확장)
- **ORM**: SQLAlchemy + Alembic
- **인증**: passlib (bcrypt)
- **환경**: python-dotenv, venv
- **테스트**: pytest
- **패키징**: PyInstaller

## 프로젝트 구조
```
boilerplate/
├── app/
│   ├── main.py          # 앱 진입점
│   ├── ui/              # UI 계층 (PyQt5 위젯·폼)
│   │   ├── login_form.py    # 로그인/회원가입 화면
│   │   ├── main_window.py   # 메인 윈도우
│   │   ├── navbar.py        # 좌측 메뉴 바
│   │   └── components.py    # 공통 컴포넌트 (토스트, 모달, 스피너)
│   ├── services/        # Service 계층 (비즈니스 로직)
│   │   └── auth_service.py  # 인증 서비스
│   ├── repositories/    # Repository 계층 (DB 접근)
│   │   └── user_repository.py  # 사용자/역할 저장소
│   ├── models/          # Model 계층 (ORM 모델)
│   │   ├── base.py          # 공통 모델 (TimestampMixin)
│   │   └── user.py          # User, Role 모델
│   ├── core/            # 핵심 인프라
│   │   ├── config.py        # 설정 관리 (.env)
│   │   ├── database.py      # DB 연결 팩토리
│   │   ├── logger.py        # 로깅 설정
│   │   ├── auth.py          # 인증 유틸 (해싱, 세션)
│   │   └── exceptions.py    # 예외 처리
│   └── resources/       # 리소스 파일
│       └── styles/          # QSS 테마 파일
│           ├── light.qss
│           └── dark.qss
├── alembic/             # DB 마이그레이션
├── .claude/             # Claude Code 설정
│   ├── settings.json        # hook 설정
│   ├── hooks/               # hook 스크립트
│   └── skills/              # 커스텀 Skill 정의
├── requirements.txt     # 패키지 목록
├── .env.example         # 환경 변수 템플릿
└── .gitignore
```

## 코딩 컨벤션
1. **계층 분리 준수**: UI → Service → Repository → Model 순서로 호출. 역방향 금지.
2. **비밀번호**: 평문 저장 절대 금지. 반드시 `hash_password()` 사용.
3. **DB 접근**: SQL 문자열 직접 결합 금지. ORM 또는 바인딩 변수 사용.
4. **시크릿**: 코드에 하드코딩 금지. `.env` 파일 사용.
5. **주석**: 비개발자 대상이므로 모든 핵심 로직에 한국어 주석 필수.
6. **임포트**: 절대 경로 사용 (`from app.core.config import ...`)

## 금지사항
- UI 코드에서 직접 DB 접근 (Repository를 거쳐야 함)
- `session.execute("SELECT ...")` 같은 원시 SQL (ORM 쿼리 사용)
- `.env` 파일을 Git에 커밋
- `print()` 디버깅 (logger 사용)
