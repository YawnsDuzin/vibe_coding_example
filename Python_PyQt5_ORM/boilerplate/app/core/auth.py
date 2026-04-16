"""
인증 모듈 (Authentication)

사용자 로그인·회원가입·비밀번호 관리·세션 상태를 담당합니다.

비개발자를 위한 설명:
- 비밀번호는 절대 원본 그대로 저장하지 않습니다 (해킹 위험)
- 대신 "해시"라는 암호화된 형태로 변환하여 저장합니다
- 로그인할 때는 입력된 비밀번호를 같은 방식으로 해시하여 비교합니다
"""
from passlib.context import CryptContext

from app.core.logger import logger

# --- 비밀번호 해싱 설정 ---
# bcrypt: 현재 가장 널리 사용되는 비밀번호 해싱 알고리즘
# deprecated="auto": 더 안전한 알고리즘이 나오면 자동 전환
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    평문 비밀번호를 해시로 변환합니다.

    Args:
        plain_password: 사용자가 입력한 비밀번호 (예: "mypassword123")

    Returns:
        해싱된 비밀번호 문자열 (예: "$2b$12$LJ3m4...")

    사용 예시 (회원가입 시):
        hashed = hash_password("사용자가 입력한 비밀번호")
        user.password_hash = hashed
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 비밀번호가 저장된 해시와 일치하는지 확인합니다.

    Args:
        plain_password: 로그인 시 사용자가 입력한 비밀번호
        hashed_password: DB에 저장된 해시값

    Returns:
        True: 비밀번호 일치
        False: 비밀번호 불일치

    사용 예시 (로그인 시):
        if verify_password("입력한 비밀번호", user.password_hash):
            print("로그인 성공!")
    """
    return pwd_context.verify(plain_password, hashed_password)


class CurrentUser:
    """
    현재 로그인한 사용자의 상태를 관리하는 클래스입니다.

    앱 전체에서 "지금 누가 로그인해 있는지"를 추적합니다.
    싱글톤 패턴으로 앱에 하나만 존재합니다.

    사용 예시:
        current = CurrentUser()
        current.login(user_obj)     # 로그인
        current.user                # 현재 사용자 객체
        current.is_logged_in        # 로그인 상태 확인
        current.has_role("admin")   # 권한 확인
        current.logout()            # 로그아웃
    """
    _instance = None

    def __new__(cls):
        # 싱글톤: 아무리 많이 생성해도 항상 같은 객체를 반환
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._user = None
        return cls._instance

    @property
    def user(self):
        """현재 로그인한 사용자 객체를 반환합니다."""
        return self._user

    @property
    def is_logged_in(self) -> bool:
        """로그인 상태 여부를 반환합니다."""
        return self._user is not None

    def login(self, user) -> None:
        """
        사용자를 로그인 상태로 설정합니다.

        Args:
            user: User 모델 객체
        """
        self._user = user
        logger.info("사용자 로그인: %s (역할: %s)", user.username, user.role.name)

    def logout(self) -> None:
        """현재 사용자를 로그아웃합니다."""
        if self._user:
            logger.info("사용자 로그아웃: %s", self._user.username)
        self._user = None

    def has_role(self, role_name: str) -> bool:
        """
        현재 사용자가 특정 역할을 가지고 있는지 확인합니다.

        Args:
            role_name: 확인할 역할 이름 ("admin", "manager", "user")

        Returns:
            True: 해당 역할을 가짐
            False: 해당 역할이 아니거나 로그인하지 않음
        """
        if not self.is_logged_in:
            return False
        return self._user.role.name == role_name
