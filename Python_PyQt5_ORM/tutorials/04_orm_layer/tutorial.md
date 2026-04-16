# 튜토리얼 4: ORM 계층 — SQLAlchemy와 Alembic

> **이 단원에서 배우는 것**: SQL 대신 Python 코드로 데이터베이스를 다루는 방법(ORM)과
> DB 구조 변경을 안전하게 관리하는 방법(Alembic)을 익힙니다.

---

## 실습 1: SQL vs ORM 비교

### 왜 ORM을 쓰나요?
ORM(Object Relational Mapping)은 "SQL을 대신 써주는 통역사"입니다.

장점:
- SQL을 몰라도 Python 코드로 DB를 다룰 수 있습니다
- **DB 교체가 쉽습니다** — SQLite에서 PostgreSQL로 바꿔도 코드 변경 최소

### Claude Code에 입력해보세요

```
app/models/user.py의 User 모델 코드를 보여주고,
이 ORM 코드가 SQL의 CREATE TABLE 문과 어떻게 대응하는지
나란히 비교하여 설명해줘.
```

### 핵심 대응표

```python
# ORM (Python 코드)                    # SQL
class User(Base):                       # CREATE TABLE users (
    __tablename__ = "users"
    id = mapped_column(Integer, PK)     #   id INTEGER PRIMARY KEY,
    username = mapped_column(String)    #   username VARCHAR(100),
    email = mapped_column(String)       #   email VARCHAR(200)
                                        # );
```

---

## 실습 2: Repository 코드 읽기

### Claude Code에 입력해보세요

```
app/repositories/user_repository.py를 읽고,
각 메서드(get_by_id, get_by_username, create, update, delete)가
SQL로 치면 어떤 쿼리에 해당하는지 비교표를 만들어줘.
```

### 세션(Session) 이해하기

```
app/core/database.py의 세션(Session) 개념을
"은행 창구" 비유로 설명해줘.
session.commit()과 session.rollback()이 각각 언제 쓰이는지 예시로 보여줘.
```

**핵심 비유**:
- `get_session()` = 은행 창구를 연다
- 작업 수행 = 거래를 한다
- `session.commit()` = 거래를 확정한다
- `session.rollback()` = 거래를 취소한다
- `session.close()` = 창구를 닫는다

---

## 실습 3: 새 모델 추가하기

### Claude Code에 입력해보세요

```
Task 모델을 만들어줘. 보일러플레이트의 User 모델과 같은 패턴으로 작성해줘.

컬럼:
- id: 자동 증가 정수 (PK)
- title: 제목 (문자열, 필수)
- description: 설명 (문자열, 선택)
- is_completed: 완료 여부 (불리언, 기본값 False)
- priority: 우선순위 (정수, 기본값 1)
- due_date: 마감일 (날짜, 선택)
- user_id: 작성자 (User 테이블의 FK)

파일 위치: app/models/task.py
TimestampMixin도 적용해줘.
```

### 검증해보세요

```
방금 만든 Task 모델을 리뷰해줘:
1. User와의 관계가 올바르게 설정되었는가?
2. TimestampMixin이 적용되었는가?
3. __tablename__이 설정되었는가?
```

---

## 실습 4: Alembic 마이그레이션 이해

### Claude Code에 입력해보세요

```
Task 모델을 추가했으니 Alembic 마이그레이션 파일을 어떻게 생성하는지 설명해줘.
마이그레이션의 upgrade()와 downgrade()가 각각 무엇을 하는지 설명해줘.
```

**핵심 비유**: Alembic = "DB 테이블의 Git"
- `alembic revision` = 변경사항을 기록 (git commit처럼)
- `alembic upgrade` = 변경사항을 적용 (앞으로)
- `alembic downgrade` = 변경사항을 되돌림 (뒤로)

---

## 이 단원을 마치며

이제 여러분은:
- ORM이 SQL의 "통역사" 역할을 한다는 것을 이해합니다
- 세션의 open → 작업 → commit/rollback → close 흐름을 이해합니다
- 새 모델을 Claude Code와 함께 추가할 수 있습니다
- Alembic 마이그레이션의 개념을 이해합니다
