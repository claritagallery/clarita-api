import logging
from os import path
from pathlib import Path

import aiosqlite

from ..config import IgnoredRoots, RootMap
from ..models import File
from . import albums, photos

logger = logging.getLogger(__name__)


class DigikamBase:
    def connect_main_db(self):
        raise NotImplementedError()

    def connect_thumbnail_db(self):
        raise NotImplementedError()

    async def albums(
        self,
        limit: int,
        offset: int,
        ignored_roots: IgnoredRoots,
        parent_album_id: int | None = None,
    ):
        async with self.connect_main_db() as db:
            return await albums.list(
                db,
                limit=limit,
                offset=offset,
                ignored_roots=ignored_roots,
                parent_album_id=parent_album_id,
            )

    async def album(self, album_id: int, ignored_roots: IgnoredRoots):
        async with self.connect_main_db() as db:
            return await albums.get(db, album_id, ignored_roots=ignored_roots)

    async def photos(
        self, limit: int, offset: int, ignored_roots: IgnoredRoots, album_id: int | None
    ):
        async with self.connect_main_db() as db:
            return await photos.list(db, limit, offset, ignored_roots, album_id)

    async def photo(self, photo_id: int, ignored_roots: IgnoredRoots):
        async with self.connect_main_db() as db:
            return await photos.get(db, photo_id, ignored_roots)

    async def photo_in_album(
        self, album_id: int, photo_id: int, ignored_roots: IgnoredRoots
    ):
        async with self.connect_main_db() as db:
            return await photos.get_in_album(db, album_id, photo_id, ignored_roots)

    async def photo_file(
        self, photo_id: int, ignored_roots: IgnoredRoots, root_map: RootMap
    ) -> File:
        async with self.connect_main_db() as db:
            return await photos.get_filepath(db, photo_id, ignored_roots, root_map)


class DigikamMySQL(DigikamBase):
    def connect_main_db(self):
        # FIXME: not implemented
        raise NotImplementedError()

    def connect_thumbnail_db(self):
        # FIXME: not implemented
        raise NotImplementedError()


class DigikamSQLite(DigikamBase):
    """Class to query a SQLite-backed Digikam DB"""

    MAIN_DB_NAME = "digikam4.db"
    THUMBNAIL_DB_NAME = "thumbnails-digikam.db"

    def __init__(
        self,
        db_root: str | Path,
        main_db_path: str | Path | None,
        thumbnail_db_path: str | Path | None,
    ):
        self.db_root = db_root
        self.main_db_path = main_db_path or path.join(db_root, self.MAIN_DB_NAME)
        self.main_db_uri = "file:{}?mode=ro".format(self.main_db_path)
        self.thumbnail_db_path = thumbnail_db_path or path.join(
            db_root, self.THUMBNAIL_DB_NAME
        )
        self.thumbnail_db_uri = "file:{}?mode=ro".format(self.thumbnail_db_path)

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

    def connect_thumbnail_db(self) -> aiosqlite.Connection:
        logger.debug(
            "Attempting to connect to thumbnail Digikam SQLite DB %s",
            self.thumbnail_db_uri,
        )
        try:
            conn = aiosqlite.connect(self.thumbnail_db_uri, uri=True)
            logger.info("Connected to thumbnail Digikam SQLite DB %s", self.main_db_uri)
        except Exception as e:
            logger.exception("Error connecting to thumbnail DB:", e)
        return conn
