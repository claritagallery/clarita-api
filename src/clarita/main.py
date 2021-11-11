from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .digikam import DigikamSQLite

ORIGINS = ["http://localhost:5000"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

digikam = DigikamSQLite("/home/fidel/digikam_data/")


@app.get("/api/v1/albums")
async def albums(
    limit: Optional[int] = 20, offset: Optional[int] = 0
) -> models.AlbumList:
    return await digikam.albums(limit, offset)


@app.get("/api/v1/album/{album_id}")
async def album(album_id: int) -> models.AlbumFull:
    return await digikam.album(album_id)


@app.get("/api/v1/album/{album_id}/photo/{photo_id}")
async def photo_in_album(album_id: int, photo_id: int):
    return await digikam.photo_in_album(album_id, photo_id)


@app.get("/api/v1/photo/{photo_id}")
async def photo(photo_id: int):
    return await digikam.photo(photo_id)
