from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: Optional[str] = None
    db_name: str

    rabbit_host: str
    rabbit_port: int
    rabbit_user: str
    rabbit_password: str

    class Config:
        env_file = ".env"


settings = Settings()
