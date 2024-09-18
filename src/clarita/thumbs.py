#!/usr/bin/env python3

import logging
from datetime import datetime
from pathlib import Path

from PIL import Image

from .config import settings
from .digikam.db import DigikamSQLite
from .models import File

logger = logging.getLogger(__name__)

THUMBS_DIR = Path(settings.clarita_data_dir) / "thumbs"
THUMBS_PER_SUBDIR = 10000
THUMB_SIZE = 300


async def get_thumbnail_file(digikam: DigikamSQLite, photo_id: int) -> File:
    """"""
    thumb_path = get_thumbnail_path(photo_id)
    if thumb_path.exists():
        # TODO: detect if photo has been modified and regenerate thumbnail
        return File(
            path=thumb_path,
            last_modified=datetime.fromtimestamp(thumb_path.stat().st_mtime),
        )
    photo_path = await digikam.photo_file(photo_id)
    thumb_path = make_thumbnail(photo_id, photo_path.path)
    return File(
        path=thumb_path,
        last_modified=datetime.fromtimestamp(thumb_path.stat().st_mtime),
    )


def get_thumbnail_path(photo_id: int) -> Path:
    """Calculate path to the thumbnail of the given photo."""
    subdir = "{:05}".format(photo_id // THUMBS_PER_SUBDIR)
    thumb_path = THUMBS_DIR / subdir / f"{photo_id}-{THUMB_SIZE}.jpg"
    return thumb_path


def make_thumbnail(photo_id: int, photo_path: str | Path):
    """Generate a thumbnail for the given photo."""
    thumb_path = get_thumbnail_path(photo_id)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        im = Image.open(photo_path)
        im.thumbnail((THUMB_SIZE, THUMB_SIZE))
        im.save(thumb_path)
        return thumb_path
    except Exception as e:
        logger.exception(
            "Error creating thumbnail for photo %s (%s): ", photo_id, photo_path, e
        )
