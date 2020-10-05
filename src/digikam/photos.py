from models import PhotoFull


async def get(db, photo_id: int):
    cursor = await db.execute(
        """
SELECT id,
       name
FROM Images
WHERE id == ?
        """,
        (photo_id,),
    )
    row = await cursor.fetchone()
    if row is None:
        return None
    return PhotoFull(
        id=row[0],
        name=row[1],
        thumb_url="https://lorempixel.com/120/120/",
        image_url="https://lorempixel.com/3000/2000/",
        prev="",
        next="",
    )
