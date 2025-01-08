import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Minha API FastAPI"
    database_url: str = "postgresql://postgres:2032@localhost:5432/WhisperAPI"

settings = Settings()

