import logging
from datetime import date
from os import path
from typing import List

from aiosqlite import Connection

from ..config import RootMap
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
    root_map: RootMap,
    parent_album_id: int | None = None,
) -> AlbumList:
    """Retrieve a list of albums.

    By default only root albums are retrieved, i.e. albums without a parent.

    Use parent_album_id to find all immediate child albums of an album.

    Parameter validation should be done in higher layers, e.g. FastAPI views.

    """
    logger.info(
        "albums list limit=%s offset=%s root_map=%r parent_album_id=%s",
        limit,
        offset,
        root_map,
        parent_album_id,
    )
    root_map_str = ",".join(str(r) for r in root_map)
    params: List[int | str] = []
    if parent_album_id is None:
        # filter root albums
        query = """
WITH album AS (SELECT a.id, a.relativePath title, a.date, a.icon
               FROM Albums a
               WHERE relativePath NOT LIKE '/%/%'
                 AND albumRoot IN (?))
"""
        params.append(root_map_str)
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
                WHERE p.id = ?
                  AND albumRoot IN (?)),
     album AS (SELECT a.id,
                      SUBSTR(a.relativePath,
                      LENGTH(parent.path)+2) title,
                      a.date,
                      a.icon
               FROM Albums a, parent
               WHERE INSTR(a.relativePath, parent.path) = 1
                 AND INSTR(title, '/') = 0
                 AND a.id <> parent.id
                 AND a.albumRoot = parent.albumRoot
                 )
"""
        params.append(parent_album_id)
        params.append(root_map_str)

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
SELECT id, title, date, icon
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
                thumb_id=None if row[3] is None else str(row[3]),
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


async def get(db, album_id: int, root_map: RootMap):
    # get album details
    logger.info("albums get album_id=%s root_map=%r", album_id, root_map)
    cursor = await db.execute(
        """
SELECT a.relativePath,
       a.date,
       COALESCE(a.caption, '') as caption,
       COALESCE(a.collection, '') as collection,
       a.icon
FROM Albums a
WHERE a.id=?
  AND albumRoot IN (?)
        """,
        (album_id, ",".join(str(r) for r in root_map)),
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
        thumb_id=None if albumrow[4] is None else str(albumrow[4]),
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
