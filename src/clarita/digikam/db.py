import logging
from pathlib import Path

import aiosqlite

from ..config import Settings
from ..models import File, Root
from ..types import AlbumOrder, PhotoOrder
from . import albums, photos, roots

logger = logging.getLogger(__name__)


class DigikamSQLite:
    """Class to query a SQLite-backed Digikam DB"""

    MAIN_DB_NAME = "digikam4.db"

    conn: aiosqlite.Connection | None = None

    def __init__(self, settings: Settings):
        self.main_db_path = Path(settings.digikam_db_dir) / self.MAIN_DB_NAME
        self.main_db_uri = "file:{}?mode=ro".format(self.main_db_path)
        self.root_map = settings.root_map

    async def connect_main_db(self):
        """Establish a new SQLite connection."""
        if self.conn is not None:
            logger.debug("Reusing existing Digikam DB connection %s", self.conn.name)
            return self.conn

        logger.debug(
            "Attempting to connect to main Digikam SQLite DB %s", self.main_db_uri
        )
        try:
            self.conn = await aiosqlite.connect(self.main_db_uri, uri=True)
            logger.info("Connected to main Digikam SQLite DB %s", self.main_db_uri)
            return self.conn
        except Exception as e:
            logger.exception("Error connecting to Digikam SQLite DB: ", e)
            raise e

    async def close(self):
        """Close underlying SQLite connection if there is one open."""
        if self.conn is not None:
            logger.debug(
                "Closing connection to main Digikam SQLite DB %s", self.main_db_uri
            )
            await self.conn.close()

    async def albums(
        self,
        limit: int,
        offset: int,
        order: AlbumOrder,
        parent_album_id: int | None = None,
    ):
        return await albums.list(
            self,
            limit=limit,
            offset=offset,
            order=order,
            parent_album_id=parent_album_id,
        )

    async def album(self, album_id: int):
        return await albums.get(self, album_id)

    async def breadcrumbs(self, album_id: int):
        return await albums.get_breadcrumbs(self, album_id)

    async def photos(
        self,
        limit: int,
        offset: int,
        order: PhotoOrder,
        album_id: int | None,
    ):
        return await photos.list(self, limit, offset, order, album_id)

    async def photo(self, photo_id: int):
        return await photos.get(self, None, photo_id)

    async def photo_in_album(self, album_id: int, photo_id: int):
        return await photos.get(self, album_id, photo_id)

    async def photo_file(self, photo_id: int) -> File:
        return await photos.get_filepath(self, photo_id)

    async def root_detail(self, root_id: int) -> Root:
        """Get all details about an album root from DB"""
        return await roots.get(self, root_id)

    async def root_path(self, root_id: int) -> str | None:
        """Get path for the given album root.

        Will favor the value in root_map if present and not empty, otherwise it will be
        retrieved from Digikam DB.

        """
        mapped_path = self.root_map.get(root_id)
        if mapped_path:
            return mapped_path

        root = await self.root_detail(root_id)
        return root.specific_path
