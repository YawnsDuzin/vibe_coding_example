"""
사용자 모델 (User Model)

사용자 정보를 데이터베이스에 저장하기 위한 ORM 모델입니다.

비개발자를 위한 설명:
- 이 파일은 "users 테이블의 설계도"입니다
- 각 변수(username, email 등)가 테이블의 컬럼(열)이 됩니다
- Python 코드로 테이블 구조를 정의하면, SQLAlchemy가 실제 DB 테이블을 만들어줍니다
"""
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Role(Base, TimestampMixin):
    """
    역할(권한 등급) 모델 — users 테이블과 1:N 관계

    3단계 권한 체계:
    - admin: 전체 관리 권한
    - manager: 관리 권한 (일부 제한)
    - user: 일반 사용자 권한
    """
    __tablename__ = "roles"  # 실제 DB 테이블 이름

    # id: 각 역할을 구분하는 고유 번호 (자동 증가)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # name: 역할 이름 (admin, manager, user)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # description: 역할에 대한 설명
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    # 관계 설정: 이 역할에 속한 사용자 목록 (1:N — 하나의 역할에 여러 사용자)
    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class User(Base, TimestampMixin):
    """
    사용자 모델 — 앱에 로그인하는 사용자 정보

    각 사용자는 반드시 하나의 역할(Role)에 속합니다.
    비밀번호는 평문이 아닌 해시값으로 저장됩니다 (보안).
    """
    __tablename__ = "users"  # 실제 DB 테이블 이름

    # id: 각 사용자를 구분하는 고유 번호 (자동 증가)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # username: 로그인 ID (중복 불가)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # email: 이메일 주소 (중복 불가)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    # password_hash: 해싱된 비밀번호 (평문 저장 금지!)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # is_active: 계정 활성 상태 (비활성화된 계정은 로그인 불가)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # role_id: 이 사용자가 속한 역할의 id (외래키)
    # ForeignKey: "roles 테이블의 id 컬럼을 참조한다"는 뜻
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)

    # 관계 설정: 이 사용자의 역할 객체에 접근 가능
    # user.role.name 으로 역할 이름을 바로 확인할 수 있습니다
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
