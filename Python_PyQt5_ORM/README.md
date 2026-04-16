# 바이브코딩(VIBE Coding) 교육 커리큘럼 — Python + PyQt5 + ORM

비개발자(기획자, PM, 디자이너, 현업 실무자)가 **AI(Claude Code)와 협업하여 자기 업무에 쓸 수 있는 데스크톱 앱을 직접 만드는** 교육 커리큘럼 + 실습 자료입니다.

---

## 바이브코딩이란?

> **"AI에게 코드를 맡기는 것"이 아니라, "AI와 협업하여 의도·설계·검증에 집중하는 것"**

| 구분 | AI(Claude Code) 담당 | 학습자 책임 |
|------|---------------------|------------|
| 의도 | 도움만 | "무엇을 왜 만드는가" 정의 |
| 설계 | 후보안 제시, 문서 초안 | 선택과 트레이드오프 판단 |
| 구현 | 코드 생성 | 결과물 읽고 검증 |
| 디버깅 | 가설 제시 | 재현 조건·증거 수집 |
| 배포 | 스크립트 제공 | 환경에서 동작 확인 |

---

## 기술 스택

| 영역 | 스택 | 역할 |
|------|------|------|
| 언어 | Python | 가장 읽기 쉬운 언어, AI가 가장 잘 생성 |
| GUI | PyQt5 + Qt Designer | 드래그앤드롭 UI 설계 |
| DB (기본) | SQLite | 설치 없이 파일 하나로 시작 |
| DB (확장) | PostgreSQL | 실전 확장 경로 |
| ORM | SQLAlchemy + Alembic | DB 독립성, 마이그레이션 |
| 개발 환경 | VSCode + Claude Code Extension | 바이브코딩 핵심 도구 |
| 패키징 | PyInstaller | 실행 파일 배포 |

---

## 저장소 구조

```
Python_PyQt5_ORM/
│
├── boilerplate/                 # 교육용 표준 보일러플레이트 (학습자 시작점)
│   ├── app/
│   │   ├── main.py              # 앱 진입점
│   │   ├── ui/                  # UI 계층 (PyQt5 위젯·폼)
│   │   │   ├── login_form.py        # 로그인/회원가입 화면
│   │   │   ├── main_window.py       # 메인 윈도우 (Navbar + 페이지)
│   │   │   ├── navbar.py            # 좌측 메뉴 바 (접기/펼치기)
│   │   │   └── components.py        # 공통 컴포넌트 (토스트, 모달, 스피너)
│   │   ├── services/            # Service 계층 (비즈니스 로직)
│   │   │   └── auth_service.py      # 인증 서비스
│   │   ├── repositories/        # Repository 계층 (DB 접근)
│   │   │   └── user_repository.py   # 사용자/역할 CRUD
│   │   ├── models/              # Model 계층 (ORM 모델)
│   │   │   ├── base.py              # TimestampMixin
│   │   │   └── user.py              # User, Role 모델
│   │   ├── core/                # 핵심 인프라
│   │   │   ├── config.py            # .env 설정 관리
│   │   │   ├── database.py          # SQLAlchemy 엔진·세션
│   │   │   ├── logger.py            # 로깅 (파일+콘솔)
│   │   │   ├── auth.py              # 비밀번호 해싱, 세션 관리
│   │   │   └── exceptions.py        # 예외 처리 유틸
│   │   └── resources/styles/    # QSS 테마
│   │       ├── light.qss            # 라이트 테마
│   │       └── dark.qss             # 다크 테마
│   ├── alembic/                 # DB 마이그레이션
│   ├── .claude/                 # Claude Code 설정
│   │   ├── settings.json            # 프롬프트 로깅 hook
│   │   ├── hooks/log-prompts.sh     # 프롬프트 자동 저장 스크립트
│   │   └── skills/                  # 커스텀 Skills (10개)
│   ├── requirements.txt         # 패키지 목록
│   ├── .env.example             # 환경 변수 템플릿
│   ├── .gitignore
│   └── CLAUDE.md                # 보일러플레이트 전용 Claude Code 가이드
│
├── curriculum/                  # 커리큘럼 설계 문서
│   ├── 00_overview.md               # 전체 개요 (10주/20회차)
│   ├── 01_dev_environment.md        # 단원 1: 개발 환경/IT 기초
│   ├── 02_python_basics.md          # 단원 2: Python 읽기
│   ├── 03_data_modeling_sql.md      # 단원 3: 데이터 모델링/SQL
│   ├── 04_orm_layer.md              # 단원 4: ORM (SQLAlchemy)
│   ├── 05_pyqt5_ui.md              # 단원 5: PyQt5 UI
│   ├── 06_requirements_to_design.md # 단원 6: 요구사항 → 설계
│   ├── 07_claude_code_env.md        # 단원 7: Claude Code 환경
│   ├── 08_ai_dev_debugging.md       # 단원 8: AI 디버깅
│   ├── 09_ai_verification.md        # 단원 9: AI 산출물 검증
│   ├── 10_deployment.md             # 단원 10: 배포
│   ├── appendix_prompt_catalog.md   # 부록 A: 프롬프트 카탈로그
│   ├── appendix_skills_reference.md # 부록 B: Skills 레퍼런스
│   └── appendix_resources.md        # 부록 C: 권장 학습 자원
│
├── tutorials/                   # 단원별 실습 튜토리얼 (코드 포함)
│   ├── 01_dev_environment/          # 환경 설정 실습
│   ├── 02_python_basics/            # Python 코드 읽기 실습
│   ├── 03_data_modeling_sql/        # ERD 설계, SQL 실습
│   ├── 04_orm_layer/                # SQLAlchemy/Alembic 실습
│   ├── 05_pyqt5_ui/                 # UI 제작 실습
│   ├── 06_requirements_design/      # PRD/설계 실습
│   ├── 07_claude_code_env/          # CLAUDE.md/Skills 실습
│   ├── 08_ai_debugging/             # 디버깅 실습
│   ├── 09_ai_verification/          # 코드 검증/pytest 실습
│   └── 10_deployment/               # PyInstaller/배포 실습
│
├── capstone/                    # 캡스톤 프로젝트 가이드
│   ├── project_a_guided.md          # A: 가이드형 (할 일 관리 앱)
│   └── project_b_autonomous.md      # B: 자율형 (나만의 업무 도구)
│
├── CLAUDE.md                    # 프로젝트 전체 Claude Code 가이드
├── vibe_coding_curriculum_prompt_final.md  # 커리큘럼 설계 원본 명세
└── _docs/                       # 보충 지시사항 및 수정 요청 노트
```

---

## 커리큘럼 구성 (10주 / 20회차)

| 주차 | 단원 | 핵심 내용 | 커스텀 Skill |
|------|------|-----------|-------------|
| 1주 | **개발 환경/IT 기초** | 터미널, Git, venv, .env | `/init-project` |
| 2주 | **Python 읽기** | 변수, 함수, 클래스, 데이터 흐름 | `/explain-code` |
| 3주 | **데이터 모델링/SQL** | ERD, 테이블, CRUD, SQLite | `/generate-erd` |
| 4주 | **ORM 계층** | SQLAlchemy, 세션, Alembic | `/create-model` |
| 5주 | **PyQt5 UI** | 위젯, 시그널/슬롯, Qt Designer | `/create-form` |
| 6주 | **요구사항 → 설계** | PRD, ERD, 아키텍처, To-do 분해 | `/plan-feature` |
| 7주 | **Claude Code 환경** | CLAUDE.md, Skills, 프롬프트 로깅 | `/analyze-prompts` |
| 8주 | **AI 디버깅** | Traceback, 프롬프팅, 버그 리포트 | `/debug` |
| 9주 | **AI 산출물 검증** | 코드 리뷰, pytest, 교차 검증 | `/review` |
| 10주 | **배포** | PyInstaller, SQLite→PostgreSQL | `/build` |

---

## 보일러플레이트 아키텍처

```
┌──────────────────────────────────────┐
│              UI 계층                  │
│  login_form │ main_window │ navbar   │
│  components (토스트, 모달, 스피너)      │
└────────────┬─────────────────────────┘
             │ 시그널/슬롯
┌────────────▼─────────────────────────┐
│           Service 계층                │
│         auth_service.py              │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│         Repository 계층               │
│       user_repository.py             │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│           Model 계층                  │
│       User │ Role │ Base             │
└────────────┬─────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│     Database (SQLite / PostgreSQL)    │
└──────────────────────────────────────┘
```

---

## 시작하기

### 1. 보일러플레이트로 프로젝트 시작

```bash
cd Python_PyQt5_ORM/boilerplate

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env

# 앱 실행
python -m app.main
```

### 2. Claude Code와 함께 학습

VSCode에서 Claude Code Extension을 설치한 후, 각 단원의 튜토리얼(`tutorials/`)을 따라하며 학습합니다.
프롬프트 카탈로그(`curriculum/appendix_prompt_catalog.md`)의 예시를 그대로 사용하거나 변형하여 Claude Code에 입력합니다.

### 3. 캡스톤 프로젝트

- **프로젝트 A (가이드형)**: `capstone/project_a_guided.md` — 할 일 관리 앱
- **프로젝트 B (자율형)**: `capstone/project_b_autonomous.md` — 자기 업무 도구

---

## 핵심 설계 원칙

1. **Claude Code-First** — 모든 작업을 Claude Code 안에서 수행
2. **구문 작성 X, 구조 이해 O** — 코드를 직접 쓰지 않고, 구조를 이해하여 정확한 프롬프트 작성
3. **보일러플레이트 기반** — 백지 시작 금지, 항상 표준 템플릿에서 출발
4. **계층 분리 준수** — UI → Service → Repository → Model 구조 일관 유지
5. **AI 산출물 검증** — 읽고 → 의심하고 → 확인하는 루틴 내재화
6. **보안 최소선** — 비밀번호 해싱, .env 시크릿, DB 바인딩 변수

---

## 대상 학습자

- 코딩 경험이 거의 없는 기획자, PM, 디자이너, 현업 실무자
- 업무 자동화나 사내 도구를 **직접** 만들고 싶은 분
- AI 도구 사용 경험은 있으나 개발 환경에 낯선 분
- 논리적 사고와 문서화 역량이 있는 분

---

## 학습 결과 (Before → After)

| Before | After |
|--------|-------|
| "터미널이 뭔가요?" | VSCode + Claude Code에서 프로젝트 관리 |
| 코드를 본 적 없음 | Python 코드를 읽고 AI에게 정확한 지시 |
| 엑셀로 데이터 관리 | ERD 설계, ORM CRUD, DB 전환 |
| "만들어줘"로 끝 | 구조적 프롬프트, AI 산출물 검증 |
| 파일명에 _v2_최종 | Git 커밋으로 버전 관리 |
| 만든 것을 공유 못 함 | PyInstaller로 실행 파일 배포 |

---

## 라이선스

교육 목적으로 자유롭게 사용할 수 있습니다.
