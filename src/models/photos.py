from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Photo(BaseModel):
    id: str
    name: str
    image_url: str
    description: Optional[str]
    # TODO: info (EXIF, etc.)
    # TODO: tags
