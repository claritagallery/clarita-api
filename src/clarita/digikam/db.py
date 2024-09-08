import logging
from functools import wraps
from pathlib import Path

import aiosqlite

from ..config import RootMap
from ..models import File
from ..types import AlbumOrder, PhotoOrder
from . import albums, photos

logger = logging.getLogger(__name__)


def require_connection(func):
    """Decorator to make sure there is a DB connection open"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.conn is None:
            await self.connect_main_db()
        return await func(self, *args, **kwargs)

    return wrapper


class DigikamSQLite:
    """Class to query a SQLite-backed Digikam DB"""

    MAIN_DB_NAME = "digikam4.db"

    conn: aiosqlite.Connection | None = None

    def __init__(self, main_db_path: str | Path):
        self.main_db_path = main_db_path
        self.main_db_uri = "file:{}?mode=ro".format(self.main_db_path)

    async def connect_main_db(self):
        """Establish a new SQLite connection."""
        logger.debug(
            "Attempting to connect to main Digikam SQLite DB %s", self.main_db_uri
        )
        try:
            self.conn = await aiosqlite.connect(self.main_db_uri, uri=True)
            assert self.conn is not None
            logger.info("Connected to main Digikam SQLite DB %s", self.main_db_uri)
        except Exception as e:
            logger.exception("Error connecting to Digikam SQLite DB:", e)
            raise e

    async def close(self):
        """Close underlying SQLite connection if there is one open."""
        if self.conn is not None:
            logger.debug(
                "Closing connection to main Digikam SQLite DB %s", self.main_db_uri
            )
            await self.conn.close()

    @require_connection
    async def albums(
        self,
        limit: int,
        offset: int,
        order: AlbumOrder,
        root_map: RootMap,
        parent_album_id: int | None = None,
    ):
        assert self.conn is not None  # silence mypy
        return await albums.list(
            self.conn,
            limit=limit,
            offset=offset,
            order=order,
            root_map=root_map,
            parent_album_id=parent_album_id,
        )

    @require_connection
    async def album(self, album_id: int, root_map: RootMap):
        assert self.conn is not None  # silence mypy
        return await albums.get(self.conn, album_id, root_map=root_map)

    @require_connection
    async def photos(
        self,
        limit: int,
        offset: int,
        order: PhotoOrder,
        root_map: RootMap,
        album_id: int | None,
    ):
        assert self.conn is not None  # silence mypy
        return await photos.list(self.conn, limit, offset, order, root_map, album_id)

    @require_connection
    async def photo(self, photo_id: int, root_map: RootMap):
        assert self.conn is not None  # silence mypy
        return await photos.get(self.conn, None, photo_id, root_map)

    @require_connection
    async def photo_in_album(self, album_id: int, photo_id: int, root_map: RootMap):
        assert self.conn is not None  # silence mypy
        return await photos.get(self.conn, album_id, photo_id, root_map)

    @require_connection
    async def photo_file(self, photo_id: int, root_map: RootMap) -> File:
        assert self.conn is not None  # silence mypy
        return await photos.get_filepath(self.conn, photo_id, root_map)
