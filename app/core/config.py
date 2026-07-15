from pydantic import (
    Field
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    secret_key: str 
    database_url: str
    debug: bool = False
    
settings = AppSettings()
    