"""
로깅 설정 모듈 (Logging Configuration)

앱에서 발생하는 이벤트를 콘솔과 파일에 기록합니다.
print() 대신 logger를 사용하면:
- 언제 발생했는지 (타임스탬프)
- 얼마나 중요한지 (레벨: DEBUG/INFO/WARNING/ERROR)
- 어디서 발생했는지 (모듈명)
를 자동으로 기록할 수 있습니다.

로그 파일은 날짜별로 분리되어 logs/ 디렉토리에 저장됩니다.
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.config import LOG_LEVEL, LOG_DIR


def setup_logger(name: str = "app") -> logging.Logger:
    """
    앱 전체에서 사용할 로거를 생성하고 설정합니다.

    Args:
        name: 로거 이름 (보통 "app" 또는 모듈명)

    Returns:
        설정이 완료된 Logger 객체

    사용 예시:
        logger = setup_logger("app")
        logger.info("앱이 시작되었습니다")
        logger.error("오류가 발생했습니다: %s", error_msg)
    """
    logger = logging.getLogger(name)

    # 이미 핸들러가 설정되어 있으면 중복 설정 방지
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # 로그 출력 형식 — 시간 | 레벨 | 모듈명 | 메시지
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- 콘솔 핸들러 ---
    # 터미널(콘솔)에 로그를 출력합니다
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- 파일 핸들러 ---
    # 로그를 파일에 저장합니다 (날짜별로 새 파일 생성)
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",       # 자정마다 새 파일 생성
        interval=1,            # 1일 간격
        backupCount=30,        # 최대 30일치 보관
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 앱 전체에서 사용할 기본 로거
logger = setup_logger("app")
