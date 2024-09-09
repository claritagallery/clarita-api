import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List

from ..exceptions import DoesNotExist, InvalidResult
from ..models import File, PhotoFull, PhotoList, PhotoShort
from ..typehint import assert_never
from ..types import PhotoOrder
from .constants import CaptionType

if TYPE_CHECKING:
    from .db import DigikamSQLite


DIGIKAM_DEFAULT_LANGUAGE = "x-default"

logger = logging.getLogger(__name__)


# This is the base query for photos that will:
# 1. Get basic data from Images table
# 2. Get creation date from ImageInformation
# 3. Get photo title from ImageComments (first one by language)
# 4. Control that photo is not part of an excluded collection (see ROOT_MAP)
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
         i.album as album,
         info.rating as rating
    FROM Images i
    LEFT JOIN first_titles d ON d.imageid=i.id
    JOIN ImageInformation info ON info.imageid=i.id
    JOIN Albums a ON a.id=i.album
   WHERE info.format='JPG'
     AND a.albumRoot IN (?)
)
"""
    % CaptionType.TITLE.value
)


async def list(
    digikam: "DigikamSQLite",
    limit: int,
    offset: int,
    order: PhotoOrder,
    album_id: int | None = None,
) -> PhotoList:
    logger.info(
        "photos list limit=%s offset=%s root_map=%r album_id=%s",
        limit,
        offset,
        digikam.root_map,
        album_id,
    )
    album_filter = "WHERE album=? " if album_id is not None else ""

    if order is PhotoOrder.titleAsc:
        order_by = "title ASC, filename ASC"
    elif order is PhotoOrder.titleDesc:
        order_by = "title DESC, filename DESC"
    elif order is PhotoOrder.dateAndTimeAsc:
        order_by = "date ASC"
    elif order is PhotoOrder.dateAndTimeDesc:
        order_by = "date DESC"
    else:
        assert_never(order)

    retrieve_query = (
        PHOTOS_QUERY
        + "SELECT * FROM photos "  # noqa: S608
        + album_filter
        + "ORDER BY %s " % order_by  # noqa: S608
        + "LIMIT ? OFFSET ?"
    )
    params: List[str | int] = [",".join(str(r) for r in digikam.root_map)]
    if album_id is not None:
        params.append(album_id)
    conn = await digikam.connect_main_db()
    cursor = await conn.execute(retrieve_query, params + [limit, offset])
    photos = []
    async for row in cursor:
        photos.append(
            PhotoShort(
                id=str(row[0]),
                filename=row[1],
                title=row[2] or row[1],
                date_and_time=row[3],
                rating=row[5],
            )
        )
    await cursor.close()
    count_query = PHOTOS_QUERY + "SELECT COUNT(*) FROM photos " + album_filter
    conn = await digikam.connect_main_db()
    cursor = await conn.execute(count_query, params)
    row = await cursor.fetchone()
    if row is None:
        raise InvalidResult()
    total = row[0]
    next_: int | None = offset + limit
    if next_ >= total:
        next_ = None
    return PhotoList(results=photos, next=next_, total=total)


async def get(digikam: "DigikamSQLite", album_id: int | None, photo_id: int):
    logger.info(
        "photo get album_id=%s photo_id=%s root_map=%r",
        album_id,
        photo_id,
        digikam.root_map,
    )
    retrieve_query = PHOTOS_QUERY + "SELECT * FROM photos WHERE id=? "
    params = [",".join(str(r) for r in digikam.root_map), photo_id]
    if album_id is not None:
        retrieve_query += "AND album=? "
        params.append(album_id)
    conn = await digikam.connect_main_db()
    cursor = await conn.execute(retrieve_query, params)
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    filename = row[1]
    title = row[2] or row[1]
    date = row[3]
    rating = row[5]

    # retrieve captions (ImageComments table)
    # there can be multiple captions, on different languages
    # default language ("x-default") will be passed as null
    cursor = await conn.execute(
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

    breadcrumbs = await digikam.breadcrumbs(album_id) if album_id else []

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
    prevnext_params = [",".join(str(r) for r in digikam.root_map), date]
    if album_id is not None:
        prevnext_params.append(album_id)
    cursor = await conn.execute(prev_query, prevnext_params)
    row = await cursor.fetchone()
    prev = None
    if row is not None:
        prev = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            title=row[2] or row[1],
            date_and_time=row[3],
            rating=row[5],
        )
    cursor = await conn.execute(next_query, prevnext_params)
    row = await cursor.fetchone()
    next_ = None
    if row is not None:
        next_ = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            title=row[2] or row[1],
            date_and_time=row[3],
            rating=row[5],
        )

    await cursor.close()

    return PhotoFull(
        id=str(photo_id),
        filename=filename,
        title=title,
        date_and_time=date,
        rating=rating,
        image_url=f"/api/v1/photos/{photo_id}/file",
        description=description,
        breadcrumbs=breadcrumbs,
        prev=prev,
        next=next_,
    )


async def get_filepath(digikam: "DigikamSQLite", photo_id: int) -> File:
    logger.info(
        "photo get_filepath photo_id=%s root_map=%r",
        photo_id,
        digikam.root_map,
    )
    conn = await digikam.connect_main_db()
    cursor = await conn.execute(
        """
SELECT a.albumRoot,
       a.relativePath,
       i.name,
       i.modificationDate
FROM Images i
JOIN Albums a ON a.id = i.album
WHERE i.id=?
  AND a.albumRoot IN (?)
        """,
        (photo_id, ",".join(str(r) for r in digikam.root_map)),
    )
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    root_id = row[0]
    root_path = await digikam.root_path(root_id)
    if not root_path:
        logger.warning("No root path for AlbumRoot id %s", root_id)
        raise DoesNotExist()

    path = Path(f"{root_path}{row[1]}/{row[2]}")
    last_modified = datetime.fromisoformat(row[3]) if row[3] else None
    return File(
        path=path,
        last_modified=last_modified,
    )
