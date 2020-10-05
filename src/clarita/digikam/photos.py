from models import Caption
from models import PhotoFull

DIGIKAM_DEFAULT_LANGUAGE = 'x-default'


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
        name=name,
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/3000/2000/",
        prev=prev_id,
        next=next_id,
    )
