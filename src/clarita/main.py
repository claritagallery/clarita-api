from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import FileResponse, JSONResponse, Response

from . import log, models
from .config import settings
from .digikam.db import DigikamSQLite
from .exceptions import DoesNotExist
from .http import HTTP_MODIFIED_DATE_FORMAT
from .thumbs import get_thumbnail_file
from .types import AlbumOrder, PhotoOrder

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


async def get_digikam():
    digikam = DigikamSQLite(settings)
    try:
        # DB connections are established on demand when first digikam method is called
        yield digikam
    finally:
        # make sure DB connections get closed
        await digikam.close()


@app.get("/api/v1/albums")
async def albums(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    parent: Annotated[int | None, Query(ge=0)] = None,
    order: Annotated[AlbumOrder, Query()] = AlbumOrder.titleAsc,
    digikam: DigikamSQLite = Depends(get_digikam),
) -> models.AlbumList:
    return await digikam.albums(limit, offset, order, parent)


@app.get("/api/v1/albums/{album_id}")
async def album(
    album_id: int,
    digikam: DigikamSQLite = Depends(get_digikam),
) -> models.AlbumFull:
    return await digikam.album(album_id)


@app.get("/api/v1/albums/{album_id}/photos/{photo_id}")
async def photo_in_album(
    album_id: int,
    photo_id: int,
    digikam: DigikamSQLite = Depends(get_digikam),
) -> models.PhotoFull:
    return await digikam.photo_in_album(album_id, photo_id)


@app.get("/api/v1/photos")
async def photos(
    album: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Annotated[PhotoOrder, Query()] = PhotoOrder.dateAndTimeAsc,
    digikam: DigikamSQLite = Depends(get_digikam),
) -> models.PhotoList:
    return await digikam.photos(limit, offset, order, album)


@app.get("/api/v1/photos/{photo_id}")
async def photo(
    photo_id: int,
    digikam: DigikamSQLite = Depends(get_digikam),
) -> models.PhotoFull:
    return await digikam.photo(photo_id)


@app.get("/api/v1/photos/{photo_id}/file", response_class=FileResponse)
async def photo_file(
    photo_id: int,
    request: Request,
    response: Response,
    digikam: DigikamSQLite = Depends(get_digikam),
):
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


@app.get("/api/v1/photos/{photo_id}/thumb", response_class=FileResponse)
async def thumb_file(
    photo_id: int,
    request: Request,
    response: Response,
    digikam: DigikamSQLite = Depends(get_digikam),
):
    thumb_file = await get_thumbnail_file(digikam, photo_id)
    return FileResponse(thumb_file.path)
