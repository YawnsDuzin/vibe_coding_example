"""
사용자 저장소 (User Repository)

사용자 데이터의 CRUD(생성·조회·수정·삭제) 작업을 담당합니다.

비개발자를 위한 설명:
- Repository는 "데이터 창고 관리인"입니다
- 데이터를 넣고, 꺼내고, 바꾸고, 지우는 작업만 합니다
- 비즈니스 판단(예: "이 사용자가 로그인할 수 있는가?")은 Service가 합니다
"""
from sqlalchemy.orm import Session

from app.models.user import User, Role
from app.core.logger import logger


class UserRepository:
    """사용자 데이터에 접근하는 저장소 클래스"""

    def __init__(self, session: Session):
        # 세션: DB와의 대화 채널 (이 채널을 통해 데이터를 주고받습니다)
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        """ID로 사용자를 조회합니다."""
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        """사용자명으로 사용자를 조회합니다."""
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User | None:
        """이메일로 사용자를 조회합니다."""
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self) -> list[User]:
        """모든 사용자 목록을 조회합니다."""
        return self.session.query(User).all()

    def create(self, user: User) -> User:
        """
        새 사용자를 생성합니다.

        Args:
            user: 저장할 User 객체

        Returns:
            DB에 저장된 User 객체 (id가 부여됨)
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        logger.info("새 사용자 생성: %s", user.username)
        return user

    def update(self, user: User) -> User:
        """사용자 정보를 수정합니다."""
        self.session.commit()
        self.session.refresh(user)
        logger.info("사용자 정보 수정: %s", user.username)
        return user

    def delete(self, user: User) -> None:
        """사용자를 삭제합니다."""
        username = user.username
        self.session.delete(user)
        self.session.commit()
        logger.info("사용자 삭제: %s", username)


class RoleRepository:
    """역할(권한) 데이터에 접근하는 저장소 클래스"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Role | None:
        """역할 이름으로 조회합니다."""
        return self.session.query(Role).filter(Role.name == name).first()

    def get_all(self) -> list[Role]:
        """모든 역할 목록을 조회합니다."""
        return self.session.query(Role).all()

    def create(self, role: Role) -> Role:
        """새 역할을 생성합니다."""
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def ensure_default_roles(self) -> None:
        """
        기본 역할(admin, manager, user)이 없으면 생성합니다.

        앱 최초 실행 시 호출하여 기본 권한 체계를 설정합니다.
        """
        default_roles = [
            ("admin", "전체 관리 권한"),
            ("manager", "관리 권한 (일부 제한)"),
            ("user", "일반 사용자 권한"),
        ]

        for role_name, description in default_roles:
            if not self.get_by_name(role_name):
                role = Role(name=role_name, description=description)
                self.session.add(role)
                logger.info("기본 역할 생성: %s", role_name)

        self.session.commit()
