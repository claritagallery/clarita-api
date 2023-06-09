import logging
from pathlib import Path

import aiosqlite

from ..config import IgnoredRoots, RootMap
from ..models import File, Thumbnail
from ..types import AlbumOrder, PhotoOrder
from . import albums, photos, thumbs

logger = logging.getLogger(__name__)


class DigikamBase:
    def connect_main_db(self):
        raise NotImplementedError()

    def connect_thumb_db(self):
        raise NotImplementedError()

    async def albums(
        self,
        limit: int,
        offset: int,
        order: AlbumOrder,
        ignored_roots: IgnoredRoots,
        parent_album_id: int | None = None,
    ):
        async with self.connect_main_db() as db:
            return await albums.list(
                db,
                limit=limit,
                offset=offset,
                order=order,
                ignored_roots=ignored_roots,
                parent_album_id=parent_album_id,
            )

    async def album(self, album_id: int, ignored_roots: IgnoredRoots):
        async with self.connect_main_db() as db:
            return await albums.get(db, album_id, ignored_roots=ignored_roots)

    async def photos(
        self,
        limit: int,
        offset: int,
        order: PhotoOrder,
        ignored_roots: IgnoredRoots,
        album_id: int | None,
    ):
        async with self.connect_main_db() as db:
            return await photos.list(db, limit, offset, order, ignored_roots, album_id)

    async def photo(self, photo_id: int, ignored_roots: IgnoredRoots):
        async with self.connect_main_db() as db:
            return await photos.get(db, None, photo_id, ignored_roots)

    async def photo_in_album(
        self, album_id: int, photo_id: int, ignored_roots: IgnoredRoots
    ):
        async with self.connect_main_db() as db:
            return await photos.get(db, album_id, photo_id, ignored_roots)

    async def photo_file(
        self, photo_id: int, ignored_roots: IgnoredRoots, root_map: RootMap
    ) -> File:
        async with self.connect_main_db() as db:
            return await photos.get_filepath(db, photo_id, ignored_roots, root_map)

    async def thumb_by_hash(self, thumb_hash: str) -> Thumbnail:
        async with self.connect_thumb_db() as db:
            return await thumbs.get_by_hash(db, thumb_hash)


class DigikamMySQL(DigikamBase):
    def connect_main_db(self):
        # FIXME: not implemented
        raise NotImplementedError()

    def connect_thumb_db(self):
        # FIXME: not implemented
        raise NotImplementedError()


class DigikamSQLite(DigikamBase):
    """Class to query a SQLite-backed Digikam DB"""

    MAIN_DB_NAME = "digikam4.db"
    THUMBNAIL_DB_NAME = "thumbnails-digikam.db"

    def __init__(
        self,
        main_db_path: str | Path,
        thumb_db_path: str | Path,
    ):
        self.main_db_path = main_db_path
        self.main_db_uri = "file:{}?mode=ro".format(self.main_db_path)
        self.thumb_db_path = thumb_db_path
        self.thumb_db_uri = "file:{}?mode=ro".format(self.thumb_db_path)

    def connect_main_db(self) -> aiosqlite.Connection:
        logger.debug(
            "Attempting to connect to main Digikam SQLite DB %s", self.main_db_uri
        )
        try:
            conn = aiosqlite.connect(self.main_db_uri, uri=True)
            logger.info("Connected to main Digikam SQLite DB %s", self.main_db_uri)
        except Exception as e:
            logger.exception("Error connecting to DB:", e)
        return conn

    def connect_thumb_db(self) -> aiosqlite.Connection:
        logger.debug(
            "Attempting to connect to thumbnail Digikam SQLite DB %s",
            self.thumb_db_uri,
        )
        try:
            conn = aiosqlite.connect(self.thumb_db_uri, uri=True)
            logger.info("Connected to thumbnail Digikam SQLite DB %s", self.thumb_db_uri)
        except Exception as e:
            logger.exception("Error connecting to thumb DB:", e)
        return conn
