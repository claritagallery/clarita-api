import logging
from functools import wraps
from pathlib import Path

import aiosqlite

from ..config import IgnoredRoots, RootMap
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
        ignored_roots: IgnoredRoots,
        parent_album_id: int | None = None,
    ):
        assert self.conn is not None  # silence mypy
        return await albums.list(
            self.conn,
            limit=limit,
            offset=offset,
            order=order,
            ignored_roots=ignored_roots,
            parent_album_id=parent_album_id,
        )

    @require_connection
    async def album(self, album_id: int, ignored_roots: IgnoredRoots):
        assert self.conn is not None  # silence mypy
        return await albums.get(self.conn, album_id, ignored_roots=ignored_roots)

    @require_connection
    async def photos(
        self,
        limit: int,
        offset: int,
        order: PhotoOrder,
        ignored_roots: IgnoredRoots,
        album_id: int | None,
    ):
        assert self.conn is not None  # silence mypy
        return await photos.list(self.conn, limit, offset, order, ignored_roots, album_id)

    @require_connection
    async def photo(self, photo_id: int, ignored_roots: IgnoredRoots):
        assert self.conn is not None  # silence mypy
        return await photos.get(self.conn, None, photo_id, ignored_roots)

    @require_connection
    async def photo_in_album(
        self, album_id: int, photo_id: int, ignored_roots: IgnoredRoots
    ):
        assert self.conn is not None  # silence mypy
        return await photos.get(self.conn, album_id, photo_id, ignored_roots)

    @require_connection
    async def photo_file(
        self, photo_id: int, ignored_roots: IgnoredRoots, root_map: RootMap
    ) -> File:
        assert self.conn is not None  # silence mypy
        return await photos.get_filepath(self.conn, photo_id, ignored_roots, root_map)
