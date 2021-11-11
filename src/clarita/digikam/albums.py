from datetime import date
from os import path
from typing import Optional

from aiosqlite import Connection

from ..models import AlbumFull, AlbumList, AlbumShort, PhotoShort


async def list(db: Connection, limit: int, offset: int) -> AlbumList:
    """Retrieve a list of albums.

    By default only root albums are retrieved, i.e. albums without a parent.

    Parameter validation should be done in higher layers, e.g. FastAPI views.

    """
    query = """
SELECT id,
       relativePath,
       date
FROM Albums
WHERE relativePath NOT LIKE '/%/%'
ORDER BY date DESC
LIMIT ?
OFFSET ?
    """
    cursor = await db.execute(query, (limit, offset))
    albums = []
    async for row in cursor:
        albums.append(
            AlbumShort(
                id=row[0],
                name=path.basename(row[1]),
                date=date.fromisoformat(row[2]),
            )
        )
    await cursor.close()
    cursor = await db.execute(
        """SELECT COUNT(*) From Albums WHERE relativePath NOT LIKE '/%/%'"""
    )
    total = (await cursor.fetchone())[0]
    next_: Optional[int] = offset + limit
    if next_ >= total:
        next_ = None
    return AlbumList(results=albums, next=next_, total=total)


async def get(db, album_id: int):
    # get album details
    cursor = await db.execute(
        """
SELECT id,
       relativePath,
       date,
       COALESCE(caption, '') as caption,
       COALESCE(collection, '') as collection
FROM Albums
WHERE id=?
        """,
        (album_id,),
    )
    albumrow = await cursor.fetchone()
    if albumrow is None:
        # no album with this id
        return None

    # get all photos in the album
    rows = await cursor.execute(
        """
SELECT i.id,
       i.name
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
WHERE i.album=?
      AND info.format='JPG'
        """,
        (album_id,),
    )
    photos = []
    async for row in rows:
        photos.append(
            PhotoShort(
                id=row[0], filename=row[1], name=row[1], thumb_url="https://lorempixel.com/120/120/"
            )
        )
    album = AlbumFull(
        id=albumrow[0],
        name=path.basename(albumrow[1]),
        thumb_url="https://lorempixel.com/120/120/",
        date=date.fromisoformat(albumrow[2]),
        description=albumrow[3],
        photos=photos,
    )

    await cursor.close()
    return album
