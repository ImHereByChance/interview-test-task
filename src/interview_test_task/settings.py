from pydantic import BaseSettings, validator
from pathlib import Path


class Settings(BaseSettings):
    SQLITE_DB_PATH: str = str(Path(__file__).parent.parent.parent / "db")

    @validator("SQLITE_DB_PATH")
    def db_path_exists(cls, db_path: str):
        if Path(db_path).exists():
            return db_path
        raise ValueError(f"path to sqlite db doesn't exist: {db_path}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
