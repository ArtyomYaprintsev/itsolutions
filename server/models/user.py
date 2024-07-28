from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.base import Base


if TYPE_CHECKING:
    from .token import Token


class User(Base):
    """Service users are represented by this model."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        index=True,
    )

    # Credentials
    email: Mapped[str] = mapped_column(sa.String(50))
    password: Mapped[str] = mapped_column(sa.String(100))

    # Internal info
    is_superuser: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=sa.func.now(),
    )

    # Relations
    tokens: Mapped[list['Token']] = relationship(
        'Token',
        back_populates='user',
    )
