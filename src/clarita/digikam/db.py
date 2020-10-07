from os import path
from pathlib import Path
from typing import Union

import aiosqlite

from . import albums
from . import photos


class DigikamBase:
    def connect_main_db(self):
        raise NotImplementedError()

    def connect_thumbnail_db(self):
        raise NotImplementedError()

    async def albums(self):
        async with self.connect_main_db() as db:
            return await albums.all(db)

    async def album(self, album_id: str):
        try:
            album_id = int(album_id)
        except ValueError:
            # Digikam albums use integer ids
            return None
        async with self.connect_main_db() as db:
            return await albums.get(db, album_id)

    async def photo(self, photo_id: str):
        try:
            photo_id = int(photo_id)
        except ValueError:
            # Digikam albums use integer ids
            return None
        async with self.connect_main_db() as db:
            return await photos.get(db, photo_id)

    async def photo_in_album(self, album_id: str, photo_id: str):
        try:
            album_id = int(album_id)
        except ValueError:
            # Digikam albums use integer ids
            return None
        try:
            photo_id = int(photo_id)
        except ValueError:
            # Digikam photos use integer ids
            return None
        async with self.connect_main_db() as db:
            return await photos.get_in_album(db, album_id, photo_id)


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

    def __init__(self, db_root: Union[str, Path]):
        self.db_root = db_root
        self.main_db_path = path.join(db_root, self.MAIN_DB_NAME)
        self.main_db_uri = "file:{}?mode=ro".format(self.main_db_path)
        self.thumbnail_db_path = path.join(db_root, self.THUMBNAIL_DB_NAME)
        self.thumbnail_db_uri = "file:{}?mode=ro".format(self.thumbnail_db_path)

    def connect_main_db(self):
        return aiosqlite.connect(self.main_db_uri, uri=True)

    def connect_thumbnail_db(self):
        return aiosqlite.connect(self.thumbnail_db_uri, uri=True)
