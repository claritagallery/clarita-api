import logging
from typing import TYPE_CHECKING

from ..exceptions import DoesNotExist
from ..models import Root

if TYPE_CHECKING:
    from .db import DigikamSQLite


logger = logging.getLogger(__name__)

ROOT_DETAIL_QUERY = """
SELECT label,
       status,
       type,
       specificPath,
       caseSensitivity
FROM AlbumRoots
WHERE id=?
"""


async def get(digikam: "DigikamSQLite", root_id: int) -> Root:
    logger.info("root get root_id=%s", root_id)
    params = [root_id]
    conn = await digikam.connect_main_db()
    cursor = await conn.execute(ROOT_DETAIL_QUERY, params)
    row = await cursor.fetchone()
    if row is None:
        raise DoesNotExist()

    label = row[0]
    status = row[1]
    type = row[2]
    specific_path = row[3]
    case_sensitivity = row[4]

    return Root(
        id=str(root_id),
        label=label,
        status=status,
        type=type,
        specific_path=specific_path,
        case_sensitivity=case_sensitivity,
    )
