from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    DATABASE_URL: str = 'sqlite+aiosqlite:///./db.sqlite3'
    SOURCE_HOST: str = 'https://www.farpost.ru'
    SYNC_ADS_SIZE: int = 10
    LIST_ADS_PATH: str = (
        '/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'
    )
    RETRIEVE_AD_PATH_PATTERN: str = '/{ad_id}'
    REQUEST_USER_AGENT: str = (
        'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )


settings = Settings()
