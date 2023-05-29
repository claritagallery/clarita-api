import logging
from datetime import date
from os import path
from typing import List

from aiosqlite import Connection

from ..config import IgnoredRoots
from ..exceptions import DoesNotExist, InvalidResult
from ..models import AlbumFull, AlbumList, AlbumShort
from ..typehint import assert_never
from ..types import AlbumOrder

logger = logging.getLogger(__name__)


async def list(
    db: Connection,
    limit: int,
    offset: int,
    order: AlbumOrder,
    ignored_roots: IgnoredRoots,
    parent_album_id: int | None = None,
) -> AlbumList:
    """Retrieve a list of albums.

    By default only root albums are retrieved, i.e. albums without a parent.

    Use parent_album_id to find all immediate child albums of an album.

    Parameter validation should be done in higher layers, e.g. FastAPI views.

    """
    logger.info(
        "albums list limit=%s offset=%s ignored_roots=%r parent_album_id=%s",
        limit,
        offset,
        ignored_roots,
        parent_album_id,
    )
    params: List[int | str] = []
    ignored_roots_str = ",".join(str(r) for r in ignored_roots) if ignored_roots else "()"
    if parent_album_id is None:
        # filter root albums
        query = """
WITH album AS (SELECT id, relativePath title, date
               FROM Albums
               WHERE relativePath NOT LIKE '/%/%'
                 AND albumRoot NOT IN (?))
"""
        params.append(ignored_roots_str)
    else:
        # Filter albums that are direct children of the given one.
        # relativePath of the parent will be something like /grandparent/parent, so
        # we use INSTR to find all other albums that start with that path
        # https://sqlite.org/lang_corefunc.html#instr
        # WITH is used to avoid repeating subqueries, the first one finds the path of the
        # parent album and the second one filters only the direct descendants (those
        # with only one / character)
        query = """
WITH parent AS (SELECT p.id, p.relativePath path, p.albumRoot
                FROM Albums p
                WHERE id = ?
                  AND albumRoot NOT IN (?)),
     album AS (SELECT a.id, SUBSTR(a.relativePath, LENGTH(parent.path)+2) title, date
               FROM Albums a, parent
               WHERE INSTR(a.relativePath, parent.path) = 1
                 AND INSTR(title, '/') = 0
                 AND a.id <> parent.id
                 AND a.albumRoot = parent.albumRoot
                 )
"""
        params.append(parent_album_id)
        params.append(ignored_roots_str)

    if order is AlbumOrder.titleAsc:
        order_by = "title ASC"
    elif order is AlbumOrder.titleDesc:
        order_by = "title DESC"
    elif order is AlbumOrder.dateAsc:
        order_by = "date ASC"
    elif order is AlbumOrder.dateDesc:
        order_by = "date DESC"
    else:
        assert_never(order)

    retrieve_query = (
        query
        + """
SELECT id, title, date
FROM album
ORDER BY %s
LIMIT ?
OFFSET ?
"""
        % order_by
    )
    cursor = await db.execute(retrieve_query, params + [limit, offset])
    albums = []
    async for row in cursor:
        albums.append(
            AlbumShort(
                id=str(row[0]),
                title=path.basename(row[1]),
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
    next_: int | None = offset + limit
    if next_ >= total:
        next_ = None
    return AlbumList(results=albums, next=next_, total=total)


async def get(db, album_id: int, ignored_roots: IgnoredRoots):
    # get album details
    logger.info("albums get album_id=%s ignored_roots=%r", album_id, ignored_roots)
    cursor = await db.execute(
        """
SELECT relativePath,
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
    full_path = albumrow[0]
    breadcrumbs = await get_breadcrumbs(db, album_id)
    album = AlbumFull(
        id=str(album_id),
        title=path.basename(full_path),
        date=date.fromisoformat(albumrow[1]),
        description=albumrow[2],
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
                title=path.basename(r[1]),
                date=date.fromisoformat(r[2]),
            )
        )
    return crumbs
