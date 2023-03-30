import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..config import IgnoredRoots, RootMap
from ..exceptions import DoesNotExist, InvalidResult
from ..models import Caption, File, PhotoFull, PhotoList, PhotoShort
from .albums import get_breadcrumbs

DIGIKAM_DEFAULT_LANGUAGE = "x-default"

logger = logging.getLogger(__name__)


async def list(
    db,
    limit: int,
    offset: int,
    ignored_roots: IgnoredRoots,
    album_id: Optional[int] = None,
) -> PhotoList:
    logger.info(
        "photos list limit=%s offset=%s ignored_roots=%r album_id=%s",
        limit,
        offset,
        ignored_roots,
        album_id,
    )
    query = """
WITH photos AS (SELECT i.id as id,
                       i.name as name,
                       info.creationDate as date
                FROM Images i
                JOIN ImageInformation info ON i.id=info.imageid
                JOIN Albums a ON a.id=i.album
                WHERE info.format='JPG'
                  AND a.albumRoot NOT IN (?)
"""
    params: List[int | str] = [",".join(str(r) for r in ignored_roots)]
    if album_id is not None:
        # filter photos by album
        query += """AND i.album=?)"""
        params.append(album_id)
    else:
        query += ")"  # close WITH clause
    retrieve_query = (
        query
        + """
SELECT id,
       name,
       date
FROM photos
ORDER BY date DESC
LIMIT ?
OFFSET ?
"""
    )
    cursor = await db.execute(retrieve_query, params + [limit, offset])
    photos = []
    async for row in cursor:
        photos.append(
            PhotoShort(
                id=str(row[0]),
                filename=row[1],
                name=row[1],
                date_and_time=row[2],
            )
        )
    await cursor.close()
    cursor = await db.execute(
        query + " SELECT COUNT(*) FROM photos",
        params,
    )
    row = await cursor.fetchone()
    if row is None:
        raise InvalidResult()
    total = row[0]
    next_: Optional[int] = offset + limit
    if next_ >= total:
        next_ = None
    return PhotoList(results=photos, next=next_, total=total)


async def get(db, photo_id: int, ignored_roots: IgnoredRoots):
    logger.info("photo get photo_id=%s ignored_roots=%r", photo_id, ignored_roots)
    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
JOIN Albums a ON a.id=i.album
WHERE i.id=?
  AND info.format='JPG'
  AND a.albumRoot NOT IN (?)
        """,
        (photo_id, ",".join(str(r) for r in ignored_roots)),
    )
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    name = row[1]
    date = row[2]

    # retrieve captions (ImageComments table)
    # there can be multiple captions, on different languages
    # default language ("x-default") will be passed as null
    cursor = await db.execute(
        """
SELECT language,
       comment
FROM ImageComments
WHERE imageid=?
        """,
        (photo_id,),
    )
    captions = []
    for r in await cursor.fetchall():
        caption = Caption(language=r[0], text=r[1].strip())
        if not caption.text:
            # there can be empty texts in the Digikam DB, ignore them
            continue
        if caption.language == DIGIKAM_DEFAULT_LANGUAGE:
            caption.language = None
        # TODO: normalize other languages to ISO 639-1
        captions.append(caption)

    # find previous and next photos by date
    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
WHERE info.creationDate<?
  AND info.format='JPG'
ORDER BY info.creationDate DESC
LIMIT 1
        """,
        (date,),
    )
    row = await cursor.fetchone()
    prev = None
    if row is not None:
        prev = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            name=row[1],
            date_and_time=row[2],
        )

    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
WHERE info.creationDate>?
  AND info.format='JPG'
ORDER BY info.creationDate ASC
LIMIT 1
        """,
        (date,),
    )
    row = await cursor.fetchone()
    next_ = None
    if row is not None:
        next_ = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            name=row[1],
            date_and_time=row[2],
        )

    await cursor.close()

    return PhotoFull(
        id=str(photo_id),
        filename=name,
        name=name,
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/1200/800/",
        breadcrumbs=[],
        prev=prev,
        next=next_,
    )


async def get_in_album(db, album_id: int, photo_id: int, ignored_roots: IgnoredRoots):
    logger.info(
        "photo get_in_album album_id=%s photo_id=%s ignored_roots=%r",
        album_id,
        photo_id,
        ignored_roots,
    )
    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN Albums a ON a.id=i.album
JOIN ImageInformation info ON i.id=info.imageid
WHERE i.id=?
  AND a.id=?
  AND info.format='JPG'
  AND a.albumRoot NOT IN (?)
        """,
        (photo_id, album_id, ",".join(str(r) for r in ignored_roots)),
    )
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    name = row[1]
    date = row[2]

    # retrieve captions (ImageComments table)
    # there can be multiple captions, on different languages
    # default language ("x-default") will be passed as null
    cursor = await db.execute(
        """
SELECT language,
       comment
FROM ImageComments
WHERE imageid=?
        """,
        (photo_id,),
    )
    captions = []
    for r in await cursor.fetchall():
        caption = Caption(language=r[0], text=r[1].strip())
        if not caption.text:
            # there can be empty texts in the Digikam DB, ignore them
            continue
        if caption.language == DIGIKAM_DEFAULT_LANGUAGE:
            caption.language = None
        # TODO: normalize other languages to ISO 639-1
        captions.append(caption)

    # find previous and next photos by date
    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN Albums a ON i.album=a.id
JOIN ImageInformation info ON i.id=info.imageid
WHERE a.id=?
  AND info.creationDate<?
  AND info.format='JPG'
ORDER BY info.creationDate DESC
LIMIT 1
        """,
        (album_id, date),
    )
    row = await cursor.fetchone()
    prev = None
    if row is not None:
        prev = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            name=row[1],
            date_and_time=row[2],
        )

    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN Albums a ON i.album=a.id
JOIN ImageInformation info ON i.id=info.imageid
WHERE a.id=?
  AND info.creationDate>?
  AND info.format='JPG'
ORDER BY info.creationDate ASC
LIMIT 1
        """,
        (album_id, date),
    )
    row = await cursor.fetchone()
    next_ = None
    if row is not None:
        next_ = PhotoShort(
            id=str(row[0]),
            filename=row[1],
            name=row[1],
            date_and_time=row[2],
        )

    await cursor.close()

    breadcrumbs = await get_breadcrumbs(db, album_id)
    return PhotoFull(
        id=str(photo_id),
        filename=name,
        name=name,
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/3000/2000/",
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
