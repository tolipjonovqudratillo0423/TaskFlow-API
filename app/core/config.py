from pydantic import Field
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent 


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )

    secret_key: str
    database_url: str
    debug: bool = False
    
    access_token_minutes: int = 30
    refresh_token_minutes: int = 7200
    
settings = AppSettings()
    