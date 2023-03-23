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


class Caption(BaseModel):
    """Description in a language.

    language will be null if not specified (default caption).

    """

    language: str | None
    text: str


class PhotoShort(BaseModel):
    """Photo to be used in list views, with just basic details"""

    id: str
    filename: str
    name: str
    date_and_time: datetime.datetime | None = None


class AlbumShort(BaseModel):
    """Album to be used in list views, with just basic details"""

    id: str
    name: str
    date: datetime.date | None = None


class PhotoFull(PhotoShort):
    """Photo to be used in detail views, with all details"""

    image_url: str
    captions: List[Caption]
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
