from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from server.db.base import Base


class Ad(Base):
    """Service ads are represented by this model."""

    __tablename__ = 'ads'

    id: Mapped[str] = mapped_column(
        sa.String(20),
        primary_key=True,
        index=True,
    )

    header: Mapped[str] = mapped_column(sa.String(250))
    address: Mapped[str] = mapped_column(
        sa.String(250),
        default=None,
        nullable=True,
    )
    author: Mapped[str] = mapped_column(
        sa.String(50),
        default=None,
        nullable=True,
    )
    author_link: Mapped[str] = mapped_column(
        sa.String(150),
        default=None,
        nullable=True,
    )
    views_count: Mapped[int] = mapped_column(sa.Integer, default=0)
    position: Mapped[int] = mapped_column(sa.Integer, default=0)

    # Internal
    is_archived: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=sa.func.now(),
    )
