from datetime import date
from os import path
from typing import Any, List, Optional

from aiosqlite import Connection

from ..exceptions import InvalidResult
from ..models import AlbumFull, AlbumList, AlbumShort, PhotoShort


async def list(
    db: Connection,
    limit: int,
    offset: int,
    parent_album_id: Optional[int] = None,
) -> AlbumList:
    """Retrieve a list of albums.

    By default only root albums are retrieved, i.e. albums without a parent.  Use
    parent_album_id to

    Parameter validation should be done in higher layers, e.g. FastAPI views.
    """
    params: List[Any] = []
    if parent_album_id is None:
        # filter root albums
        query = """
WITH album AS (SELECT id, relativePath path, date
               FROM Albums
               WHERE relativePath NOT LIKE '/%/%')
"""
    else:
        # Filter albums that are direct children of the given one.
        # relativePath of the parent will be something like /grandparent/parent, so
        # use INSTR to find all other albums that start with that path
        # https://sqlite.org/lang_corefunc.html#instr
        # WITH is used to avoid repeating subqueries, the first one has the path of the
        # parent album and the second one filters only the direct descendants (those
        # with only one / character)
        query = """
WITH parent AS (SELECT p.relativePath path
                FROM Albums p
                WHERE p.id = ?),
     album AS (SELECT a.id, SUBSTR(a.relativePath, LENGTH(parent.path)+2) path, date
               FROM Albums a, parent
               WHERE INSTR(a.relativePath, parent.path) == 1
                 AND (LENGTH(path)-LENGTH(REPLACE(path, '/', ''))) = 1)
"""
        params.append(parent_album_id)
    retrieve_query = (
        query
        + """
SELECT id, path, date
FROM album
ORDER BY date DESC
LIMIT ?
OFFSET ?
"""
    )
    cursor = await db.execute(retrieve_query, params + [limit, offset])
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
        query + " SELECT COUNT(*) FROM album",
        params,
    )
    row = await cursor.fetchone()
    if row is None:
        raise InvalidResult()
    total = row[0]
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
                id=row[0],
                filename=row[1],
                name=row[1],
                thumb_url="https://lorempixel.com/120/120/",
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
