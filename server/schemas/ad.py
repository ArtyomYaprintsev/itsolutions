from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_serializer


class BaseAd(BaseModel):
    """Base Ad model scheme."""
    id: str
    header: str
    is_archived: bool


class AdAuthor(BaseModel):
    """Ad model scheme with author fields only.

    Provides additional field serializer for `author_link` field.
    """
    author: str | None = None
    author_link: HttpUrl | None = None

    @field_serializer('author_link')
    def serialize_author_link(self, author_link: HttpUrl | None):
        """Serialize author link."""
        return str(author_link) if author_link else author_link


class Ad(BaseAd, AdAuthor):
    """Ad model scheme."""
    address: str | None = None
    views_count: int = 0
    position: int = 0
    updated_at: datetime | None = None


class UpdateAd(BaseModel):
    """Update Ad model scheme."""
    header: str | None = None
    address: str | None = None
    author: str | None = None
    author_link: HttpUrl | None = None
    views_count: int | None = None
    position: int | None = None
    is_archived: bool | None = None
