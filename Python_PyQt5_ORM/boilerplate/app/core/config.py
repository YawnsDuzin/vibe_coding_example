"""
설정 관리 모듈 (Configuration)

.env 파일에서 앱 설정값을 읽어와 Python 코드에서 사용할 수 있게 합니다.
모든 설정은 이 모듈을 통해 접근합니다 — 코드 곳곳에 설정값을 흩뿌리지 않습니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드 — 프로젝트 루트의 .env 파일에서 환경 변수를 읽어옵니다
# 이 한 줄이 .env 파일의 모든 값을 os.environ에 등록합니다
load_dotenv()

# --- 프로젝트 경로 ---
# 이 파일(config.py)로부터 프로젝트 루트 경로를 역산합니다
# config.py → core/ → app/ → boilerplate/ (프로젝트 루트)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- 앱 기본 설정 ---
APP_NAME = os.getenv("APP_NAME", "바이브코딩 앱")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# --- 데이터베이스 설정 ---
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # "sqlite" 또는 "postgresql"

# SQLite 설정
SQLITE_DB_PATH = BASE_DIR / os.getenv("SQLITE_DB_PATH", "data/app.db")

# PostgreSQL 설정
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "vibe_coding_db")
PG_USER = os.getenv("PG_USER", "")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

# --- 로깅 설정 ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / os.getenv("LOG_DIR", "logs")


def get_database_url() -> str:
    """
    DB_TYPE에 따라 적절한 데이터베이스 연결 URL을 반환합니다.

    SQLAlchemy는 URL 문자열로 어떤 데이터베이스에 접속할지 결정합니다.
    .env 파일의 DB_TYPE 값만 바꾸면 SQLite ↔ PostgreSQL 전환이 가능합니다.
    """
    if DB_TYPE == "postgresql":
        # PostgreSQL URL 형식: postgresql://사용자:비밀번호@호스트:포트/데이터베이스명
        return f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    else:
        # SQLite URL 형식: sqlite:///파일경로
        # 파일이 없으면 자동으로 생성됩니다
        SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{SQLITE_DB_PATH}"
