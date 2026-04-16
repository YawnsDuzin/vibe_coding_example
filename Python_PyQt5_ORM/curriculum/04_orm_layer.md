# 단원 4: ORM 계층 — SQLAlchemy와 Alembic

| 항목 | 내용 |
|------|------|
| **주차** | 4주 (7~8회차) |
| **예상 시간** | 6시간 (강의 2h + 실습 4h) |
| **보일러플레이트 연결** | `app/models/`, `app/repositories/`, `alembic/` |

---

## 학습 목표 (3개)

1. ORM이 무엇인지 이해하고, SQL과 ORM 코드를 비교하여 대응 관계를 설명할 수 있다
2. SQLAlchemy 모델과 세션 개념을 이해하고, Repository 코드를 읽고 검증할 수 있다
3. Alembic 마이그레이션의 필요성을 체감하고, Claude Code로 마이그레이션을 생성·실행할 수 있다

---

## 주요 내용

### 4.1 ORM이란?
- "SQL을 직접 쓰지 않고 Python 코드로 DB를 다루는 도구"
- 비유: "외국어(SQL)를 통역사(ORM)가 대신 말해주는 것"
- **핵심 장점**: DB 종류를 바꿔도 코드를 거의 수정하지 않음 (DB 독립성)

### 4.2 SQL ↔ ORM 대응표
| SQL | SQLAlchemy ORM |
|-----|---------------|
| `CREATE TABLE users (...)` | `class User(Base): __tablename__ = "users"` |
| `INSERT INTO users VALUES (...)` | `session.add(user)` |
| `SELECT * FROM users WHERE id=1` | `session.query(User).filter(User.id==1).first()` |
| `UPDATE users SET name='...'` | `user.name = '...'` + `session.commit()` |
| `DELETE FROM users WHERE id=1` | `session.delete(user)` + `session.commit()` |

### 4.3 세션(Session) 이해
- "은행 창구" 비유: 창구를 열고 → 거래하고 → 확정(commit)하고 → 창구를 닫는 흐름
- `session.commit()`: 변경사항 확정 (거래 완료)
- `session.rollback()`: 변경사항 취소 (거래 취소)
- `session.close()`: 창구 닫기

### 4.4 Repository 패턴
- 보일러플레이트의 `user_repository.py` 읽기
- "데이터 창고 관리인" — CRUD만 담당, 비즈니스 판단은 Service에서

### 4.5 Alembic 마이그레이션
- "DB 테이블의 Git" — 변경 이력을 관리
- `alembic revision --autogenerate`: 변경사항 감지하여 마이그레이션 파일 생성
- `alembic upgrade head`: 마이그레이션 적용
- `alembic downgrade -1`: 마이그레이션 되돌리기

### 4.6 DB 독립성 체험
- `.env`에서 `DB_TYPE=sqlite` → `DB_TYPE=postgresql` 전환
- "코드를 한 줄도 안 바꿨는데 다른 DB에서 동작한다!"

---

## AI 협업 방식

| Claude Code가 하는 것 | 학습자가 하는 것 |
|----------------------|-----------------|
| SQL DDL → SQLAlchemy 모델 변환 | ORM 코드와 원본 SQL을 비교하며 대응 관계 이해 |
| Repository 클래스 생성 | CRUD 메서드가 올바른 SQL로 변환되는지 확인 |
| Alembic 마이그레이션 파일 생성 | 생성된 마이그레이션의 upgrade/downgrade 내용 검토 |

---

## 프롬프트 카탈로그

```
이 CREATE TABLE 문을 SQLAlchemy 모델로 변환해줘. 원본 SQL과 ORM 코드를 나란히 보여주고 대응 관계를 설명해줘.
```

```
Task 모델에 대한 Repository 클래스를 만들어줘. user_repository.py와 같은 패턴으로 CRUD 메서드를 구현해줘.
```

```
Task 모델을 추가했으니 Alembic 마이그레이션 파일을 생성해줘. 마이그레이션 파일의 내용을 설명해줘.
```

---

## 커스텀 Skill 명세

### `/create-model`
| 항목 | 내용 |
|------|------|
| **용도** | 테이블 스키마 → SQLAlchemy 모델 + Repository + 마이그레이션 스캐폴딩 |
| **입력** | 테이블명, 컬럼 목록, 관계 정보 |
| **출력** | 모델 파일 + Repository 파일 + Alembic 마이그레이션 가이드 |
| **정의 위치** | `.claude/skills/create-model/SKILL.md` |

---

## 자주 만나는 함정

### 함정 1: "객체인지 테이블인지 헷갈려요"
- **증상**: `User` 클래스가 Python 객체인 건지, DB 테이블인 건지 혼란
- **완화법**: "User 클래스는 설계도, DB 테이블은 그 설계도로 만든 실제 창고"
  - `user = User(username="홍길동")` → "설계도로 '홍길동' 카드를 만든 것"
  - `session.add(user)` → "카드를 창고에 넣은 것"
  - `session.commit()` → "창고 문을 잠근 것(확정)"

### 함정 2: "session.commit()을 깜빡했어요"
- **증상**: 데이터를 수정했는데 DB에 반영이 안 됨
- **완화법**: "commit은 저장 버튼" — 엑셀에서 Ctrl+S 안 누르면 날아가는 것과 같음
  - Repository 코드의 패턴을 따르면 commit을 빼먹을 일 없음

---

## 완료 기준 (자가진단 체크리스트)

- [ ] ORM이 무엇이고 왜 사용하는지 설명할 수 있다
- [ ] SQL의 INSERT/SELECT/UPDATE/DELETE가 ORM에서 어떻게 표현되는지 비교할 수 있다
- [ ] session.commit()과 session.rollback()의 역할을 설명할 수 있다
- [ ] 보일러플레이트의 `user_repository.py`를 읽고 각 메서드가 하는 일을 설명할 수 있다
- [ ] Claude Code로 새 모델을 추가하고 Alembic 마이그레이션을 생성할 수 있다
