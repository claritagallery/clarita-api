from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

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
    limit: int = 20,
    offset: int = 0,
    parent: Optional[int] = None,
) -> models.AlbumList:
    return await digikam.albums(limit, offset, parent)


@app.get("/api/v1/album/{album_id}")
async def album(album_id: int) -> models.AlbumFull:
    return await digikam.album(album_id)


@app.get("/api/v1/album/{album_id}/photo/{photo_id}")
async def photo_in_album(album_id: int, photo_id: int):
    return await digikam.photo_in_album(album_id, photo_id)


@app.get("/api/v1/photo/{photo_id}")
async def photo(photo_id: int):
    return await digikam.photo(photo_id)


@app.get("/api/v1/photo/{photo_id}/file")
async def photo_file(photo_id: int):
    path = await digikam.photo_file(photo_id)
    return FileResponse(path)


@app.get("/api/v1/photos")
async def photos(
    album: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> models.PhotoList:
    return await digikam.photos(album, limit, offset)
