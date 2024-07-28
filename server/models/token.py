from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.db.base import Base
from server.tools.code import generate_str_code


if TYPE_CHECKING:
    from .user import User


class Token(Base):
    """Service auth tokens are represented by this model."""

    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(
        sa.String(40),
        unique=True,
        default=lambda: generate_str_code(20),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=sa.func.now(),
    )

    # Relations
    user: Mapped['User'] = relationship('User', back_populates='tokens')
