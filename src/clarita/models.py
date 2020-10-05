from datetime import date
from typing import List
from typing import Optional

from pydantic import BaseModel


class Caption(BaseModel):
    """Description in a language.

    language will be null if not specified (default caption).

    """

    language: Optional[str]
    text: str


class PhotoShort(BaseModel):
    """Photo to be used in list views, with just basic details"""

    id: str
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
    thumb_url: Optional[str]
    date: Optional[date]


class AlbumFull(AlbumShort):
    """Album to be used in detail views, with all details"""

    description: str
    photos: List[PhotoShort]
