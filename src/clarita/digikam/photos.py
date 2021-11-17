from typing import Optional

from ..exceptions import InvalidResult
from ..models import Caption, PhotoFull, PhotoList, PhotoShort
from .albums import get_breadcrumbs

DIGIKAM_DEFAULT_LANGUAGE = "x-default"


async def list(db, limit: int, offset: int, album_id: Optional[int] = None) -> PhotoList:
    query = """
WITH photos AS (SELECT i.id as id,
                       i.name as name,
                       info.creationDate as date
                FROM Images i
                JOIN ImageInformation info ON i.id=info.imageid
                WHERE info.format='JPG'
"""
    params = []
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
ORDER BY date
LIMIT ?
OFFSET ?
"""
    )
    cursor = await db.execute(retrieve_query, params + [limit, offset])
    photos = []
    async for row in cursor:
        photos.append(
            PhotoShort(
                id=row[0],
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


async def get(db, photo_id: int):
    cursor = await db.execute(
        """
SELECT i.id,
       i.name,
       info.creationDate
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
WHERE i.id=?
  AND info.format='JPG'
        """,
        (photo_id,),
    )
    row = await cursor.fetchone()
    if row is None:
        return None

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
SELECT i.id
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
    prev_id = row[0] if row is not None else None

    cursor = await db.execute(
        """
SELECT i.id
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
    next_id = row[0] if row is not None else None

    await cursor.close()

    return PhotoFull(
        id=photo_id,
        filename=name,
        name=name,
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/1200/800/",
        prev=prev_id,
        next=next_id,
    )


async def get_in_album(db, album_id: int, photo_id: int):
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
        """,
        (photo_id, album_id),
    )
    row = await cursor.fetchone()
    if row is None:
        return None

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
            id=row[0],
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
            id=row[0],
            filename=row[1],
            name=row[1],
            date_and_time=row[2],
        )

    await cursor.close()

    breadcrumbs = await get_breadcrumbs(db, album_id)
    return PhotoFull(
        id=photo_id,
        filename=name,
        name=name,
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/3000/2000/",
        breadcrumbs=breadcrumbs,
        prev=prev,
        next=next_,
    )
