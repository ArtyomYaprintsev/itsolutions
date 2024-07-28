from datetime import datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    """Base User model scheme."""
    id: int
    email: str
    is_superuser: bool = False


class InternalUser(BaseUser):
    """User scheme with internal data."""
    joined_at: datetime
    is_active: bool = True
    is_superuser: bool = False
