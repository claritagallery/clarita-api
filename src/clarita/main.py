from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import FileResponse, JSONResponse, Response

from . import log, models
from .config import settings
from .digikam import DigikamSQLite
from .exceptions import DoesNotExist
from .http import HTTP_MODIFIED_DATE_FORMAT

log.setup_logging()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DoesNotExist)
async def does_not_exist_exception_handler(request: Request, exc: DoesNotExist):
    return JSONResponse(
        status_code=404,
        content="Not found",
    )


digikam = DigikamSQLite(
    settings.database_root,
    settings.database_main_path,
    settings.database_thumbnail_path,
)


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
async def photo_in_album(album_id: int, photo_id: int) -> models.PhotoFull:
    return await digikam.photo_in_album(album_id, photo_id)


@app.get("/api/v1/photo/{photo_id}")
async def photo(photo_id: int) -> models.PhotoFull:
    return await digikam.photo(photo_id)


@app.get("/api/v1/photo/{photo_id}/file")
async def photo_file(photo_id: int, request: Request, response: Response):
    photo_file = await digikam.photo_file(photo_id)
    last_modified = photo_file.last_modified
    if last_modified:
        response.headers["Last-Modified"] = last_modified.strftime(
            HTTP_MODIFIED_DATE_FORMAT
        )
        if if_modified_since_raw := request.headers.get("If-Modified-Since"):
            if if_modified_since := datetime.strptime(
                if_modified_since_raw, HTTP_MODIFIED_DATE_FORMAT
            ):
                if last_modified >= if_modified_since:
                    return Response(status_code=304)
    return FileResponse(photo_file.path)


@app.get("/api/v1/photos")
async def photos(
    album: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> models.PhotoList:
    return await digikam.photos(album, limit, offset)
