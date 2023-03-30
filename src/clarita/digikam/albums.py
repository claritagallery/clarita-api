import logging
from datetime import date
from os import path
from typing import Any, List, Optional

from aiosqlite import Connection

from ..config import IgnoredRoots
from ..exceptions import DoesNotExist, InvalidResult
from ..models import AlbumFull, AlbumList, AlbumShort

logger = logging.getLogger(__name__)


async def list(
    db: Connection,
    limit: int,
    offset: int,
    ignored_roots: IgnoredRoots,
    parent_album_id: Optional[int] = None,
) -> AlbumList:
    """Retrieve a list of albums.

    By default only root albums are retrieved, i.e. albums without a parent.  Use
    parent_album_id to

    Parameter validation should be done in higher layers, e.g. FastAPI views.
    """
    logger.info(
        "albums list limit=%s offset=%s ignored_roots=%r parent_album_id=%s",
        limit,
        offset,
        ignored_roots,
        parent_album_id,
    )
    params: List[Any] = []
    ignored_roots_str = ",".join(str(r) for r in ignored_roots) if ignored_roots else "()"
    if parent_album_id is None:
        # filter root albums
        query = """
WITH album AS (SELECT id, relativePath path, date
               FROM Albums
               WHERE relativePath NOT LIKE '/%/%'
                 AND albumRoot NOT IN (?))
"""
        params.append(ignored_roots_str)
    else:
        # Filter albums that are direct children of the given one.
        # relativePath of the parent will be something like /grandparent/parent, so
        # use INSTR to find all other albums that start with that path
        # https://sqlite.org/lang_corefunc.html#instr
        # WITH is used to avoid repeating subqueries, the first one has the path of the
        # parent album and the second one filters only the direct descendants (those
        # with only one / character)
        query = """
WITH parent AS (SELECT p.id, p.relativePath path
                FROM Albums p
                WHERE p.id = ?),
     album AS (SELECT a.id, SUBSTR(a.relativePath, LENGTH(parent.path)+2) path, date
               FROM Albums a, parent
               WHERE INSTR(a.relativePath, parent.path) == 1
                 AND (LENGTH(path)-LENGTH(REPLACE(path, '/', ''))) = 1
                 AND a.id <> parent.id
                 AND albumRoot NOT IN (?))
"""
        params.append(parent_album_id)
        params.append(ignored_roots_str)
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
                id=str(row[0]),
                name=path.basename(row[1]),
                date=date.fromisoformat(row[2]),
            )
        )
    await cursor.close()
    cursor = await db.execute(
        query + " SELECT COUNT(*) FROM album",
        params,
    )
    count = await cursor.fetchone()
    if count is None:
        raise InvalidResult()
    total = count[0]
    next_: Optional[int] = offset + limit
    if next_ >= total:
        next_ = None
    return AlbumList(results=albums, next=next_, total=total)


async def get(db, album_id: int, ignored_roots: IgnoredRoots):
    # get album details
    logger.info("albums get album_id=%s ignored_roots=%r", album_id, ignored_roots)
    cursor = await db.execute(
        """
SELECT id,
       relativePath,
       date,
       COALESCE(caption, '') as caption,
       COALESCE(collection, '') as collection
FROM Albums
WHERE id=?
  AND albumRoot NOT IN (?)
        """,
        (album_id, ",".join(str(r) for r in ignored_roots)),
    )
    albumrow = await cursor.fetchone()
    if albumrow is None:
        raise DoesNotExist()
    album_id = albumrow[0]
    full_path = albumrow[1]
    breadcrumbs = await get_breadcrumbs(db, album_id)
    album = AlbumFull(
        id=str(album_id),
        name=path.basename(full_path),
        thumb_url="https://lorempixel.com/120/120/",
        date=date.fromisoformat(albumrow[2]),
        description=albumrow[3],
        breadcrumbs=breadcrumbs,
    )

    await cursor.close()
    return album


async def get_breadcrumbs(db, album_id: int) -> List[AlbumShort]:
    """Find all albums that are ancestors of the given one"""
    logger.info("albums get_breadcrumbs album_id=%s", album_id)
    cursor = await db.execute(
        """
WITH parent AS (SELECT p.relativePath path
                FROM Albums p
                WHERE p.id = ?)
SELECT id,
       relativePath,
       date
FROM Albums, parent
WHERE INSTR(parent.path, relativePath)
  AND relativePath <> '/'
ORDER BY LENGTH(relativePath)
        """,
        (album_id,),
    )
    crumbs = []
    for r in await cursor.fetchall():
        crumbs.append(
            AlbumShort(
                id=str(r[0]),
                name=path.basename(r[1]),
                date=date.fromisoformat(r[2]),
            )
        )
    return crumbs
