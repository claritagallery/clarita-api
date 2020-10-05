from models import Caption
from models import PhotoFull

DIGIKAM_DEFAULT_LANGUAGE = 'x-default'


async def get(db, photo_id: int):
    cursor = await db.execute(
        """
SELECT i.id,
       i.name
FROM Images i
JOIN ImageInformation info ON i.id=info.imageid
WHERE i.id=?
  AND info.format='JPG'
        """,
        (photo_id,),
    )
    photorow = await cursor.fetchone()
    if photorow is None:
        return None

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

    await cursor.close()

    return PhotoFull(
        id=photorow[0],
        name=photorow[1],
        captions=captions,
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/3000/2000/",
        prev="",
        next="",
    )
