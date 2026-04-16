# 튜토리얼 2: Python 기본 문법 — 읽기와 이해

> **이 단원에서 배우는 것**: Python 코드를 읽고 "무슨 일이 일어나는지" 이해하는 능력을 키웁니다.
> 코드를 직접 작성하는 것이 아니라 **읽고 검증하는 것**에 집중합니다.

---

## 핵심 원칙

> 비개발자에게 Python 문법을 "외우세요"라고 하지 않습니다.
> 대신 "이 코드가 뭘 하는지 대충 읽을 수 있으면" 충분합니다.
> 구문 작성은 Claude Code가 하고, 여러분은 읽고 검증합니다.

---

## 실습 1: 변수 — "이름이 붙은 상자"

### Claude Code에 입력해보세요

```
변수가 무엇인지 "택배 상자" 비유로 설명해줘.
보일러플레이트의 app/core/config.py에서 변수 사용 예시를 찾아 설명해줘.
```

### 보일러플레이트에서 확인

`app/core/config.py`에서 이런 코드를 볼 수 있습니다:

```python
# APP_NAME이라는 상자에 "바이브코딩 앱"이라는 값을 넣습니다
APP_NAME = os.getenv("APP_NAME", "바이브코딩 앱")

# DB_TYPE이라는 상자에 "sqlite"라는 값을 넣습니다
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
```

### 이해 확인
Claude Code에 물어보세요:
```
config.py에서 os.getenv("APP_NAME", "바이브코딩 앱")이 하는 일을 설명해줘.
첫 번째 인자와 두 번째 인자가 각각 무엇인지 알려줘.
```

**답**: `.env` 파일에서 `APP_NAME` 값을 찾고, 없으면 `"바이브코딩 앱"`을 기본값으로 사용합니다.

---

## 실습 2: 함수 — "입력 → 처리 → 출력 기계"

### Claude Code에 입력해보세요

```
app/core/auth.py의 hash_password 함수가 하는 일을
비개발자가 이해할 수 있게 한 줄씩 설명해줘.
"입력 → 처리 → 출력" 구조로 정리해줘.
```

### 보일러플레이트에서 확인

```python
def hash_password(plain_password: str) -> str:
    """평문 비밀번호를 해시로 변환합니다."""
    return pwd_context.hash(plain_password)
```

이 함수를 "기계"에 비유하면:
- **입력**: 평문 비밀번호 (예: "mypassword123")
- **처리**: bcrypt 알고리즘으로 암호화
- **출력**: 해싱된 문자열 (예: "$2b$12$LJ3m4...")

### 검증 포인트 ✓
- [ ] `def`는 "함수를 정의한다"는 뜻이라는 것을 이해하나요?
- [ ] `return`은 "결과를 돌려준다"는 뜻이라는 것을 이해하나요?

---

## 실습 3: 클래스 — "설계도와 제품"

### Claude Code에 입력해보세요

```
app/models/user.py의 User 클래스를 "자동차 설계도" 비유로 설명해줘.
클래스(설계도)와 객체(실제 자동차)의 차이를 보여줘.
```

### 핵심 이해

```python
# 이것은 "설계도" (클래스)
class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = ...
    username = ...
    email = ...

# 이것은 "설계도로 만든 실제 제품" (객체)
user = User(username="홍길동", email="hong@test.com", ...)
```

비유:
- `class User` = 자동차 설계도
- `user = User(...)` = 설계도로 만든 실제 자동차 1대
- `user.username` = 이 자동차의 색상 (속성)

---

## 실습 4: 데이터 흐름 추적하기

### Claude Code에 입력해보세요

```
사용자가 회원가입할 때 데이터가 어떻게 흘러가는지 추적해줘.
auth_service.py의 register 메서드부터 시작해서,
user_repository.py를 거쳐 user.py까지의 흐름을 단계별로 설명해줘.
```

### 데이터 흐름 요약

```
사용자 입력 (이름, 이메일, 비밀번호)
    ↓
AuthService.register()  ← 비즈니스 판단 (중복 확인, 비밀번호 해싱)
    ↓
UserRepository.create()  ← 데이터 저장 (DB에 넣기)
    ↓
User 모델  ← 테이블 구조 정의
    ↓
데이터베이스 (SQLite 파일)
```

### 검증 포인트 ✓
- [ ] 왜 UI에서 바로 DB에 접근하지 않고 Service → Repository를 거치는지 설명할 수 있나요?
- [ ] 비밀번호가 어느 시점에서 해싱되는지 찾을 수 있나요?

---

## 이 단원을 마치며

이제 여러분은 Python 코드를 읽을 수 있습니다!
- 변수 = 이름 붙은 상자
- 함수 = 입력 → 처리 → 출력 기계
- 클래스 = 설계도
- import = 다른 파일에서 도구 가져오기

**기억하세요**: 코드를 "작성"할 필요는 없습니다.
Claude Code가 작성하면, 여러분은 **읽고 검증**하면 됩니다.
