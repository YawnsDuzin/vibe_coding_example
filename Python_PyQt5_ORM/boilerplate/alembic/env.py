"""
Alembic 환경 설정 (Migration Environment)

이 파일은 Alembic이 마이그레이션을 실행할 때 사용하는 설정입니다.
.env 파일의 DB 설정을 읽어서 Alembic이 올바른 데이터베이스에 접속하도록 합니다.

비개발자를 위한 설명:
- 마이그레이션(Migration): DB 테이블 구조를 변경하는 작업
  (예: 새 컬럼 추가, 테이블 생성 등)
- 이 파일은 직접 수정할 일이 거의 없습니다
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- 앱의 설정과 모델을 가져옵니다 ---
from app.core.config import get_database_url
from app.core.database import Base
# 모든 모델을 import해야 Alembic이 테이블 변경을 감지할 수 있습니다
import app.models  # noqa: F401

# Alembic Config 객체 — alembic.ini의 값에 접근합니다
config = context.config

# .env 파일의 DB URL로 덮어쓰기 — 이렇게 하면 alembic.ini를 수정하지 않아도 됩니다
config.set_main_option("sqlalchemy.url", get_database_url())

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic이 추적할 메타데이터 — Base에 등록된 모든 모델의 테이블 정보
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """오프라인 모드로 마이그레이션 실행 (DB 접속 없이 SQL만 생성)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """온라인 모드로 마이그레이션 실행 (DB에 직접 접속하여 변경 적용)"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
