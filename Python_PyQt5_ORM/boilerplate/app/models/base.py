"""
모델 기본 클래스 (Model Base)

모든 ORM 모델이 공통으로 가지는 컬럼(id, 생성일, 수정일)을 정의합니다.
새 모델을 만들 때 이 클래스를 상속받으면 공통 컬럼을 자동으로 갖게 됩니다.
"""
from datetime import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampMixin:
    """
    타임스탬프 믹스인 — 생성일과 수정일을 자동 관리합니다.

    비개발자를 위한 설명:
    - created_at: 이 데이터가 처음 만들어진 시각 (자동 기록)
    - updated_at: 이 데이터가 마지막으로 수정된 시각 (자동 갱신)
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),  # DB가 자동으로 현재 시각 입력
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),  # 수정될 때마다 자동 갱신
    )
