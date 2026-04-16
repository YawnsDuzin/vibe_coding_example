# 부록 B: 커스텀 Skills 레퍼런스

커리큘럼 전체에서 사용되는 10개 커스텀 Skill의 요약입니다.
각 Skill의 상세 정의는 `.claude/skills/<이름>/SKILL.md`에 있습니다.

---

## Skills 목록

| # | Skill명 | 용도 | 사용 단원 |
|---|---------|------|----------|
| 1 | `/init-project` | 프로젝트 초기 환경 설정 (venv, pip, Git, .env) | 단원 1 |
| 2 | `/explain-code` | 코드를 비개발자 눈높이로 줄별 해설 | 단원 2, 전체 |
| 3 | `/generate-erd` | 자연어 요구사항 → Mermaid ERD + DDL 생성 | 단원 3, 6 |
| 4 | `/create-model` | 테이블 스키마 → SQLAlchemy 모델 + Repository | 단원 4, 캡스톤 |
| 5 | `/create-form` | 폼 사양 → PyQt5 위젯 클래스 + 시그널/슬롯 | 단원 5, 캡스톤 |
| 6 | `/plan-feature` | 기능 설명 → PRD + ERD + 작업 분해 | 단원 6, 캡스톤 |
| 7 | `/analyze-prompts` | 프롬프트 로그 분석 → Skill 후보 추천 | 단원 7 |
| 8 | `/debug` | 에러 분석 → 원인 진단 → 수정 제안 | 단원 8, 전체 |
| 9 | `/review` | 코드 리뷰 + 보안 확인 + 테스트 커버리지 | 단원 9, 전체 |
| 10 | `/build` | PyInstaller 빌드 → 실행 파일 생성 | 단원 10 |

---

## Skill 파일 구조

```
.claude/skills/
├── init-project/SKILL.md
├── explain-code/SKILL.md
├── generate-erd/SKILL.md
├── create-model/SKILL.md
├── create-form/SKILL.md
├── plan-feature/SKILL.md
├── analyze-prompts/SKILL.md
├── debug/SKILL.md
├── review/SKILL.md
└── build/SKILL.md
```

---

## Skill 제작 가이드

학습자가 자신만의 Skill을 만들고 싶을 때 따르는 단계:

1. **반복 패턴 발견**: 같은 형태의 프롬프트를 3회 이상 사용했나요?
2. **패턴 구조화**: 변하는 부분(입력)과 변하지 않는 부분(틀)을 분리
3. **SKILL.md 작성**: 용도, 실행 내용, 입력/출력을 명시
4. **등록**: `.claude/skills/<이름>/SKILL.md`에 파일 생성
5. **테스트**: 다양한 입력으로 Skill이 올바르게 동작하는지 확인
6. **개선**: 사용하면서 부족한 부분을 보완
