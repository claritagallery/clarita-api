from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import BaseModel


class ListResponse(BaseModel):
    """Generic response for a list with limit and offset"""

    next: Optional[int]
    total: int


class Caption(BaseModel):
    """Description in a language.

    language will be null if not specified (default caption).

    """

    language: Optional[str]
    text: str


class PhotoShort(BaseModel):
    """Photo to be used in list views, with just basic details"""

    id: str
    filename: str
    name: str
    thumb_url: str


class PhotoFull(PhotoShort):
    """Photo to be used in detail views, with all details"""

    image_url: str
    captions: List[Caption]
    prev: Optional[str]
    next: Optional[str]
    # TODO: Exif info
    # TODO: tags
    # TODO: copyright


class AlbumShort(BaseModel):
    """Album to be used in list views, with just basic details"""

    id: str
    name: str
    date: Optional[datetime.date] = None


class AlbumFull(AlbumShort):
    """Album to be used in detail views, with all details"""

    description: str
    breadcrumbs: List[AlbumShort]


class AlbumList(ListResponse):
    """Response for a list of albums"""

    results: List[AlbumShort]
