from typing import Dict, List

from pydantic_settings import BaseSettings, SettingsConfigDict

RootMap = Dict[int, str]


class Settings(BaseSettings):
    cors_origins: List[str]

    database_main_path: str
    database_thumbnail_path: str

    error_log_filename: str | None = None
    loglevel_clarita: str = "INFO"
    loglevel_root: str = "INFO"

    # Map paths of Digikam DB AlbumRoots to potentially new locations.
    # Only roots listed here will be served by Clarita, others will be filtered out.
    # Use an empty string "" to use the DB value for the root.
    # Otherwise value should be the absolute path for files in the system Clarita
    # is running on.
    root_map: RootMap = {}

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
