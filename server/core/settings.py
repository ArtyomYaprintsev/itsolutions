from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    DATABASE_URL: str = 'sqlite+aiosqlite:///./db.sqlite3'


settings = Settings()
