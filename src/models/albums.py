from datetime import date
from typing import Optional

from pydantic import BaseModel


class Album(BaseModel):
    id: str
    name: str
    thumb_url: Optional[str]
    date: Optional[date]
    description: Optional[str]
