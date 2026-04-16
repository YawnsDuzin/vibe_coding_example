"""
데이터베이스 연결 팩토리 (Database Connection Factory)

SQLAlchemy 엔진과 세션을 생성·관리합니다.
앱 전체에서 이 모듈을 통해 DB에 접근합니다.

핵심 개념:
- Engine(엔진): 데이터베이스와의 연결을 관리하는 객체
- Session(세션): 데이터를 읽고 쓰는 작업 단위 (은행 창구와 비슷)
- 세션을 열고 → 작업하고 → 커밋(저장)하고 → 닫는 흐름입니다
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from app.core.config import get_database_url


class Base(DeclarativeBase):
    """
    모든 ORM 모델의 부모 클래스입니다.

    SQLAlchemy에서 데이터베이스 테이블을 Python 클래스로 표현할 때,
    모든 모델은 이 Base 클래스를 상속받아야 합니다.
    Base가 모든 모델을 추적하여 테이블을 자동으로 생성할 수 있게 합니다.
    """
    pass


# --- 엔진 생성 ---
# create_engine: 데이터베이스 연결을 설정합니다
# echo=False: SQL 쿼리를 콘솔에 출력하지 않음 (디버깅 시 True로 변경)
engine = create_engine(
    get_database_url(),
    echo=False,
)

# --- 세션 팩토리 ---
# sessionmaker: 세션을 만드는 '공장'을 설정합니다
# autocommit=False: 명시적으로 commit()을 호출해야 저장됩니다 (안전장치)
# autoflush=False: 쿼리 실행 시 자동으로 DB에 반영하지 않음
SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    """
    새로운 데이터베이스 세션을 생성하여 반환합니다.

    사용 예시:
        session = get_session()
        try:
            # 데이터 읽기/쓰기 작업
            session.commit()  # 변경사항 저장
        except Exception:
            session.rollback()  # 오류 시 되돌리기
        finally:
            session.close()    # 세션 닫기
    """
    return SessionFactory()


def init_db():
    """
    데이터베이스 테이블을 초기화합니다.

    Base를 상속받은 모든 모델의 테이블을 자동으로 생성합니다.
    이미 존재하는 테이블은 건드리지 않습니다 (checkfirst=True 기본값).

    주의: 프로덕션에서는 Alembic 마이그레이션을 사용하세요.
    이 함수는 초기 개발/학습 용도입니다.
    """
    Base.metadata.create_all(bind=engine)
