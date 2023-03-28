from typing import Dict, List, Set

from pydantic import BaseSettings

IgnoredRoots = Set[int]
RootMap = Dict[int, str]


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
    # map paths of AlbumRoots to new locations
    # use when the location of actual files are different on the server running Clarita
    root_map: RootMap = {}


settings = Settings()
