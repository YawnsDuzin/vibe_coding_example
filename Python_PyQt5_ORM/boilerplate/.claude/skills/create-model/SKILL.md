# /create-model

테이블 스키마를 SQLAlchemy 모델 + Repository + 마이그레이션으로 변환하는 Skill입니다.

## 용도
테이블 정보를 입력하면 보일러플레이트 패턴에 맞는 모델, Repository, 마이그레이션 가이드를 생성합니다.

## 실행 내용

1. **모델 파일 생성**: `app/models/<이름>.py`
   - Base 상속, TimestampMixin 적용
   - 각 컬럼에 한국어 주석
   - 관계(relationship) 설정
2. **Repository 파일 생성**: `app/repositories/<이름>_repository.py`
   - user_repository.py와 동일한 패턴으로 CRUD 메서드
3. **models/__init__.py 업데이트**: 새 모델 import 추가
4. **Alembic 마이그레이션 안내**: 마이그레이션 생성 명령과 확인 방법

## 입력 예시
```
테이블명: tasks
컬럼: title(문자열,필수), description(문자열), is_completed(불리언,기본False), priority(정수,기본1), due_date(날짜), user_id(FK→users)
```

## 사용되는 단원
- 단원 4: ORM 계층
- 캡스톤 프로젝트
