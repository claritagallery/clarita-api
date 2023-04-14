import logging
from datetime import datetime
from pathlib import Path
from typing import List

from ..config import IgnoredRoots, RootMap
from ..exceptions import DoesNotExist, InvalidResult
from ..models import File, PhotoFull, PhotoList, PhotoShort
from .albums import get_breadcrumbs
from .constants import CaptionType

DIGIKAM_DEFAULT_LANGUAGE = "x-default"

logger = logging.getLogger(__name__)


# This is the base query for photos that will:
# 1. Get basic data from Images table
# 2. Get creation date from ImageInformation
# 3. Get photo title from ImageComments (first one by language)
# 4. Control that photo is not part of an excluded collection (see IGNORED_ROOTS)
PHOTOS_QUERY = (
    """
WITH numbered_titles AS (
  SELECT *,
         ROW_NUMBER() OVER (
            PARTITION BY imageid
            ORDER BY language asc
        ) AS row_number
    FROM ImageComments
   WHERE type=%d
), first_titles AS (
    SELECT *
    FROM numbered_titles
    WHERE row_number = 1
), photos AS (
  SELECT i.id as id,
         i.name as filename,
         d.comment as title,
         info.creationDate as date,
         i.album as album
    FROM Images i
    LEFT JOIN first_titles d ON d.imageid=i.id
    JOIN ImageInformation info ON info.imageid=i.id
    JOIN Albums a ON a.id=i.album
   WHERE info.format='JPG'
     AND a.albumRoot NOT IN (?)
)
"""
    % CaptionType.TITLE.value
)


async def list(
    db,
    limit: int,
    offset: int,
    ignored_roots: IgnoredRoots,
    album_id: int | None = None,
) -> PhotoList:
    logger.info(
        "photos list limit=%s offset=%s ignored_roots=%r album_id=%s",
        limit,
        offset,
        ignored_roots,
        album_id,
    )
    album_filter = "WHERE album=? " if album_id is not None else ""
    retrieve_query = (
        PHOTOS_QUERY
        + "SELECT * FROM photos "
        + album_filter
        + "ORDER BY date DESC "
        + "LIMIT ? OFFSET ?"
    )
    params: List[str | int] = [",".join(str(r) for r in ignored_roots)]
    if album_id is not None:
        params.append(album_id)
    cursor = await db.execute(retrieve_query, params + [limit, offset])
    photos = []
    async for row in cursor:
        photos.append(
            PhotoShort(
                id=str(row[0]),
                filename=row[1],
                title=row[2] or row[1],
                date_and_time=row[3],
            )
        )
    await cursor.close()
    count_query = PHOTOS_QUERY + "SELECT COUNT(*) FROM photos " + album_filter
    cursor = await db.execute(count_query, params)
    row = await cursor.fetchone()
    if row is None:
        raise InvalidResult()
    total = row[0]
    next_: int | None = offset + limit
    if next_ >= total:
        next_ = None
    return PhotoList(results=photos, next=next_, total=total)


async def get(db, album_id: int | None, photo_id: int, ignored_roots: IgnoredRoots):
    logger.info(
        "photo get album_id=%s photo_id=%s ignored_roots=%r",
        album_id,
        photo_id,
        ignored_roots,
    )
    retrieve_query = PHOTOS_QUERY + "SELECT * FROM photos WHERE id=? "
    params = [",".join(str(r) for r in ignored_roots), photo_id]
    if album_id is not None:
        retrieve_query += "AND album=? "
        params.append(album_id)
    cursor = await db.execute(retrieve_query, params)
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    filename = row[1]
    title = row[2] or row[1]
    date = row[3]

    # retrieve captions (ImageComments table)
    # there can be multiple captions, on different languages
    # default language ("x-default") will be passed as null
    cursor = await db.execute(
        """
SELECT language,
       comment
  FROM ImageComments
 WHERE imageid=?
   AND type=?
ORDER BY language ASC
LIMIT 1
        """,
        (photo_id, CaptionType.DESCRIPTION.value),
    )
    description = ""
    rows = await cursor.fetchall()
    logger.debug("Available descriptions for photo %s: %r", photo_id, rows)
    description = rows[0][1] if rows else ""

    breadcrumbs = await get_breadcrumbs(db, album_id) if album_id else []

    # find previous and next photos by date
    prev_query = (
        PHOTOS_QUERY
        + "SELECT * FROM photos WHERE date<? "
        + ("AND album=? " if album_id is not None else "")
        + "ORDER BY date DESC LIMIT 1"
    )
    next_query = (
        PHOTOS_QUERY
        + "SELECT * FROM photos WHERE date>? "
        + ("AND album=? " if album_id is not None else "")
        + "ORDER BY date ASC LIMIT 1"
    )
    prevnext_params = [",".join(str(r) for r in ignored_roots), date]
    if album_id is not None:
        prevnext_params.append(album_id)
    cursor = await db.execute(prev_query, prevnext_params)
    row = await cursor.fetchone()
    prev = None
    if row is not None:
        prev = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            title=row[2] or row[1],
            date_and_time=row[3],
        )
    cursor = await db.execute(next_query, prevnext_params)
    row = await cursor.fetchone()
    next_ = None
    if row is not None:
        next_ = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            title=row[2] or row[1],
            date_and_time=row[3],
        )

    await cursor.close()

    return PhotoFull(
        id=str(photo_id),
        filename=filename,
        title=title,
        date_and_time=date,
        image_url=f"/api/v1/photos/{photo_id}/file",
        description=description,
        breadcrumbs=breadcrumbs,
        prev=prev,
        next=next_,
    )


async def get_filepath(
    db, photo_id: int, ignored_roots: IgnoredRoots, root_map: RootMap
) -> File:
    logger.info(
        "photo get_filepath photo_id=%s ignored_roots=%r root_map=%r",
        photo_id,
        ignored_roots,
        root_map,
    )
    cursor = await db.execute(
        """
SELECT r.id,
       r.specificPath,
       a.relativePath,
       i.name,
       i.modificationDate
FROM Images i
JOIN Albums a ON a.id = i.album
JOIN AlbumRoots r ON a.albumRoot
WHERE i.id=?
  AND a.albumRoot NOT IN (?)
        """,
        (photo_id, ",".join(str(r) for r in ignored_roots)),
    )
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()
    root_id = row[0]
    root_path = root_map.get(root_id, row[1])
    path = Path(f"{root_path}{row[2]}/{row[3]}")
    last_modified = datetime.fromisoformat(row[4]) if row[4] else None
    return File(
        path=path,
        last_modified=last_modified,
    )
