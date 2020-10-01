from datetime import date
from os import path

from models.albums import Album


async def get_all(db):
    cursor = await db.execute(
        """
SELECT id,
       relativePath,
       COALESCE(caption, '') as caption,
       COALESCE(collection, '') as collection,
       date
FROM Albums
ORDER BY id
        """
    )
    rows = await cursor.fetchall()
    albums = []
    for row in rows:
        albums.append(
            Album(
                id=row[0],
                name=path.basename(row[1]),
                description=row[2],
                date=date.fromisoformat(row[4]),
            )
        )
    await cursor.close()
    return albums
