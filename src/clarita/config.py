from typing import List, Set

from pydantic import BaseSettings

IgnoredRoots = Set[int]


class Settings(BaseSettings):
    cors_origins: List[str]

    database_root: str
    database_main_path: str
    database_thumbnail_path: str

    error_log_filename: str = "error.log"
    loglevel_clarita: str = "INFO"
    loglevel_root: str = "INFO"

    # ids of AlbumRoots to ignore
    ignored_roots: IgnoredRoots = set()


settings = Settings()
