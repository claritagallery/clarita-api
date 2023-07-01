from __future__ import annotations

import datetime
from pathlib import Path
from typing import List

from pydantic import BaseModel


class ListResponse(BaseModel):
    """Generic response for a list with limit and offset"""

    next: int | None
    total: int


class File(BaseModel):
    path: Path
    last_modified: datetime.datetime | None


class PhotoShort(BaseModel):
    """Photo to be used in list views, with just basic details"""

    id: str
    filename: str
    title: str
    date_and_time: datetime.datetime | None = None
    rating: int
    thumb_hash: str


class AlbumShort(BaseModel):
    """Album to be used in list views, with just basic details"""

    id: str
    title: str
    date: datetime.date | None = None
    thumb_hash: str | None = None


class PhotoFull(PhotoShort):
    """Photo to be used in detail views, with all details"""

    image_url: str
    description: str
    breadcrumbs: List[AlbumShort]
    prev: PhotoShort | None
    next: PhotoShort | None
    # TODO: Exif info
    # TODO: tags
    # TODO: copyright


class AlbumFull(AlbumShort):
    """Album to be used in detail views, with all details"""

    description: str
    breadcrumbs: List[AlbumShort]


class PhotoList(ListResponse):
    """Response for a list of photos"""

    results: List[PhotoShort]


class AlbumList(ListResponse):
    """Response for a list of albums"""

    results: List[AlbumShort]


class Thumbnail(BaseModel):
    data: bytes
    last_modified: datetime.datetime
    orientation: int
    unique_hash: str
