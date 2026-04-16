"""
인증 서비스 (Authentication Service)

로그인·회원가입의 비즈니스 로직을 담당합니다.

비개발자를 위한 설명:
- Service는 "비즈니스 판단"을 하는 계층입니다
- "이 사용자명은 이미 사용 중인가?", "비밀번호가 맞는가?" 같은 판단을 합니다
- Repository에서 데이터를 가져와 판단하고, 결과를 UI에 전달합니다

계층 흐름: UI(화면) → Service(판단) → Repository(데이터 접근) → Model(DB 테이블)
"""
from app.core.auth import hash_password, verify_password, CurrentUser
from app.core.database import get_session
from app.core.exceptions import AppError
from app.core.logger import logger
from app.models.user import User
from app.repositories.user_repository import UserRepository, RoleRepository


class AuthService:
    """로그인·회원가입 비즈니스 로직을 처리하는 서비스"""

    def register(
        self,
        username: str,
        email: str,
        password: str,
        role_name: str = "user",
    ) -> User:
        """
        새 사용자를 등록(회원가입)합니다.

        Args:
            username: 사용자명 (중복 불가)
            email: 이메일 (중복 불가)
            password: 비밀번호 (해싱되어 저장됨)
            role_name: 역할 이름 (기본값: "user")

        Returns:
            생성된 User 객체

        Raises:
            AppError: 사용자명/이메일 중복, 역할 미존재 시
        """
        session = get_session()
        try:
            user_repo = UserRepository(session)
            role_repo = RoleRepository(session)

            # 사용자명 중복 확인
            if user_repo.get_by_username(username):
                raise AppError("이미 사용 중인 사용자명입니다.", code="DUPLICATE_USERNAME")

            # 이메일 중복 확인
            if user_repo.get_by_email(email):
                raise AppError("이미 사용 중인 이메일입니다.", code="DUPLICATE_EMAIL")

            # 역할 조회
            role = role_repo.get_by_name(role_name)
            if not role:
                raise AppError(f"존재하지 않는 역할입니다: {role_name}", code="ROLE_NOT_FOUND")

            # 새 사용자 생성 — 비밀번호는 해시로 변환하여 저장
            user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role_id=role.id,
            )
            user = user_repo.create(user)
            logger.info("회원가입 완료: %s (역할: %s)", username, role_name)
            return user

        except AppError:
            raise
        except Exception as e:
            session.rollback()
            logger.error("회원가입 실패: %s", str(e))
            raise AppError("회원가입 중 오류가 발생했습니다.", code="REGISTER_ERROR")
        finally:
            session.close()

    def login(self, username: str, password: str) -> User:
        """
        사용자 로그인을 처리합니다.

        Args:
            username: 사용자명
            password: 비밀번호

        Returns:
            인증된 User 객체

        Raises:
            AppError: 사용자 미존재, 비밀번호 불일치, 비활성 계정 시
        """
        session = get_session()
        try:
            user_repo = UserRepository(session)
            user = user_repo.get_by_username(username)

            # 사용자 존재 확인
            if not user:
                raise AppError("사용자를 찾을 수 없습니다.", code="USER_NOT_FOUND")

            # 계정 활성 상태 확인
            if not user.is_active:
                raise AppError("비활성화된 계정입니다.", code="ACCOUNT_INACTIVE")

            # 비밀번호 확인
            if not verify_password(password, user.password_hash):
                raise AppError("비밀번호가 일치하지 않습니다.", code="WRONG_PASSWORD")

            # 로그인 성공 — 현재 사용자 상태 설정
            CurrentUser().login(user)
            logger.info("로그인 성공: %s", username)
            return user

        except AppError:
            raise
        except Exception as e:
            logger.error("로그인 실패: %s", str(e))
            raise AppError("로그인 중 오류가 발생했습니다.", code="LOGIN_ERROR")
        finally:
            session.close()

    def logout(self) -> None:
        """현재 사용자를 로그아웃합니다."""
        CurrentUser().logout()
