from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    cors_origins: List[str]
    error_log_filename: str = "error.log"
    loglevel_clarita: str = "INFO"
    loglevel_root: str = "INFO"


settings = Settings()
