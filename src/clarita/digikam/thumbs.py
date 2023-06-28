import logging
from datetime import datetime

from ..exceptions import DoesNotExist
from ..models import Thumbnail

logger = logging.getLogger(__name__)


async def get_by_hash(db, thumb_hash: str) -> Thumbnail:
    logger.info("thumbs get_by_hash thumb_hash=%s", thumb_hash)
    cursor = await db.execute(
        """
SELECT t.modificationDate,
       t.orientationHint,
       t.data
FROM Thumbnails t
JOIN UniqueHashes h ON t.id = h.thumbId
WHERE h.uniqueHash=?
        """,
        (thumb_hash,),
    )
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()
    last_modified = datetime.fromisoformat(row[0])
    orientation = row[1]
    data = row[2]
    return Thumbnail(
        data=data,
        last_modified=last_modified,
        orientation=orientation,
        unique_hash=thumb_hash,
    )
