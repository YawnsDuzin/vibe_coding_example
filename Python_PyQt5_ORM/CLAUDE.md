# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

비개발자(기획자, PM, 디자이너, 현업 실무자) 대상의 **바이브코딩(VIBE Coding) 튜토리얼** 저장소입니다. 커리큘럼 설계 문서를 기반으로 **실제 동작하는 코드와 단계별 실습 자료**를 제작합니다.

- 모든 문서·주석·커밋 메시지는 **한국어**로 작성, 기술 용어는 영문 병기
- 학습자의 개발 환경: **VSCode + Claude Code Extension**

## 저장소 구조

- `vibe_coding_curriculum_prompt_final.md` — 커리큘럼 설계 명세 (단일 원천, 모든 튜토리얼의 근거)
- `_docs/` — 보충 지시사항 및 수정 요청 노트

향후 추가될 구조:
```
boilerplate/           # 교육용 표준 보일러플레이트 (학습자 시작점)
  app/
    ui/                # PyQt 위젯·폼
    services/          # 비즈니스 로직
    repositories/      # ORM 쿼리
    models/            # SQLAlchemy 모델
    core/              # 설정·로깅·인증
    resources/         # .ui, .qss, 아이콘
tutorials/             # 단원별 튜토리얼 (문서 + 코드)
skills/                # Claude Code 커스텀 Skill 정의 파일
capstone/              # 캡스톤 프로젝트 가이드 및 예제
```

## 바이브코딩 핵심 철학

**"AI에게 코드를 맡기는 것"이 아니라 "AI와 협업하여 학습자가 의도·설계·검증에 집중하는 것"**

| 구분 | AI(Claude Code) 담당 | 학습자 책임 |
|---|---|---|
| 의도 | 도움만 | "무엇을 왜 만드는가" 정의 |
| 설계 | 후보안 제시, 문서 초안 | 선택과 트레이드오프 판단 |
| 구현 | 코드 생성 | 결과물 읽고 검증 |
| 문서화 | PRD·ERD·설정 파일 초안 | 내용 검토·수정·확정 |
| 학습 | 개념 설명, 예제 생성 | 이해 확인·질문·반복 연습 |
| 디버깅 | 가설 제시 | 재현 조건·증거 수집 |
| 배포 | 스크립트 제공 | 환경에서 동작 확인 |

## 고정 기술 스택 (변경 불가)

Python, PyQt5 + Qt Designer, SQLite(MVP) → PostgreSQL(확장), SQLAlchemy + Alembic, VSCode + Claude Code Extension, PyInstaller, Git, venv, pytest, python-dotenv, logging

## 설계 원칙

1. **DB 독립성** — ORM 계층을 통해 SQLite→PostgreSQL 전환이 자연스럽도록 설계
2. **UI-로직 분리** — PyQt5 시그널/슬롯을 초반부터 도입
3. **환경 재현성** — venv + requirements.txt + .env를 기본 습관으로 교육
4. **AI 산출물 검증** — 모든 실습에 읽기/실행/확인 루틴 삽입
5. **롤백 가능성** — Git 커밋을 되돌릴 수 있는 최소 단위로 훈련
6. **보안 최소선** — 비밀번호 해싱, .env 시크릿 관리, DB 바인딩 변수 사용
7. **Claude Code 전 과정 활용** — 코드뿐 아니라 문법 학습, SQL, 문서 작성, 설정, 디버깅 등 모든 작업을 Claude Code로 수행. 프롬프트 문서화 및 반복 패턴의 커스텀 Skill化

## 튜토리얼 코드 작성 규칙

튜토리얼 코드를 작성할 때 반드시 지키는 규칙:

- **비개발자 대상**: 코드의 모든 핵심 라인에 한국어 주석 필수. "왜 이렇게 하는가"를 설명
- **보일러플레이트 기반**: 모든 실습은 `boilerplate/` 구조에서 출발. 백지 시작 금지
- **점진적 확장**: 각 튜토리얼은 이전 단계의 코드 위에 기능을 추가하는 방식
- **실행 가능**: 모든 코드 예제는 독립적으로 실행 가능해야 함. 미완성 스니펫 금지
- **프롬프트 포함**: 각 실습 단계에서 학습자가 Claude Code에 입력할 프롬프트 예시 제공
- **검증 루틴 포함**: AI가 생성한 코드를 학습자가 직접 확인하는 체크포인트 삽입
- **계층 분리 준수**: UI → Service → Repository → Model 구조를 항상 유지

## 커스텀 Skills 작성 규칙

- Skill 정의 파일은 `.claude/skills/` 또는 프로젝트 `skills/` 디렉토리에 저장
- 각 Skill에는 용도, 입력/출력, 사용 단원을 명시
- 주요 Skill 후보: `/init-project`, `/explain-code`, `/generate-erd`, `/create-model`, `/create-form`, `/plan-feature`, `/debug`, `/review`, `/build`, `/analyze-prompts`

## 프롬프트 로깅 & Skill 추천 워크플로

보일러플레이트에 `UserPromptSubmit` hook이 미리 설정되어 있어 모든 프롬프트가 `.claude/prompt-log.jsonl`에 자동 저장됩니다. 이 로그를 활용한 워크플로:

1. **자동 수집**: hook이 프롬프트를 타임스탬프·세션ID와 함께 기록
2. **패턴 분석**: `/analyze-prompts` Skill로 반복 패턴 분석 → Skill 후보 추천
3. **Skill 제작**: 추천된 패턴을 `.claude/skills/<name>/SKILL.md`로 제작

`.claude/prompt-log.jsonl`은 `.gitignore` 대상 (민감 정보 보호)
