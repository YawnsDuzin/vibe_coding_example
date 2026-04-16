"""
예외 처리 유틸리티 (Exception Handling Utilities)

앱에서 발생하는 오류를 안전하게 처리하는 도구들입니다.

비개발자를 위한 설명:
- 프로그램은 실행 중 예상치 못한 상황(예외)을 만날 수 있습니다
- 예외를 처리하지 않으면 프로그램이 갑자기 종료됩니다
- 이 모듈의 도구를 사용하면 오류가 나도 프로그램이 계속 동작하고,
  무엇이 잘못되었는지 로그에 기록됩니다
"""
import functools
import traceback

from app.core.logger import logger


def safe_execute(func):
    """
    함수 실행 중 오류가 발생해도 프로그램이 멈추지 않게 보호하는 데코레이터입니다.

    사용법 — 보호하고 싶은 함수 위에 @safe_execute를 붙입니다:

        @safe_execute
        def save_data():
            # 이 안에서 오류가 나도 프로그램이 멈추지 않습니다
            ...

    오류 발생 시:
    - 오류 내용이 로그에 자동 기록됩니다
    - 함수는 None을 반환합니다
    - 프로그램은 계속 동작합니다
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 오류의 전체 경로(Traceback)를 로그에 기록
            logger.error(
                "오류 발생 [%s]: %s\n%s",
                func.__name__,
                str(e),
                traceback.format_exc(),
            )
            return None
    return wrapper


class AppError(Exception):
    """
    앱 고유의 예외 클래스입니다.

    일반적인 오류와 구분하여, 앱에서 의도적으로 발생시키는 오류를 표현합니다.

    사용 예시:
        raise AppError("사용자를 찾을 수 없습니다", code="USER_NOT_FOUND")
    """

    def __init__(self, message: str, code: str = "UNKNOWN"):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        return f"[{self.code}] {self.message}"
