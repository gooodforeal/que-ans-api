from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/que_ans_db"
    project_name: str = "Questions and Answers API"
    api_version: str = "1.0.0"
    debug: bool = False
    cors_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
