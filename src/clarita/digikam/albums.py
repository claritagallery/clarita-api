from datetime import date
from os import path

from models import AlbumFull, AlbumShort, PhotoShort


async def all(db):
    cursor = await db.execute(
        """
SELECT id,
       relativePath,
       date
FROM Albums
ORDER BY id
        """
    )
    albums = []
    async for row in cursor:
        albums.append(
            AlbumShort(
                id=row[0],
                name=path.basename(row[1]),
                thumb_url="https://lorempixel.com/120/120/",
                date=date.fromisoformat(row[2]),
            )
        )
    await cursor.close()
    return albums


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
            PhotoShort(id=row[0], name=row[1], thumb_url="https://lorempixel.com/120/120/")
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
