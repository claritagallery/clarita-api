from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import FileResponse, JSONResponse, Response

from . import log, models
from .config import settings
from .digikam.db import DigikamSQLite
from .exceptions import DoesNotExist
from .http import HTTP_MODIFIED_DATE_FORMAT
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


digikam = DigikamSQLite(
    settings.database_main_path,
    settings.database_thumbnail_path,
)


@app.get("/api/v1/albums")
async def albums(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    parent: Annotated[int | None, Query(ge=0)] = None,
    order: Annotated[AlbumOrder, Query()] = AlbumOrder.titleAsc,
) -> models.AlbumList:
    return await digikam.albums(limit, offset, order, settings.ignored_roots, parent)


@app.get("/api/v1/albums/{album_id}")
async def album(album_id: int) -> models.AlbumFull:
    return await digikam.album(album_id, settings.ignored_roots)


@app.get("/api/v1/albums/{album_id}/photos/{photo_id}")
async def photo_in_album(album_id: int, photo_id: int) -> models.PhotoFull:
    return await digikam.photo_in_album(album_id, photo_id, settings.ignored_roots)


@app.get("/api/v1/photos")
async def photos(
    album: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Annotated[PhotoOrder, Query()] = PhotoOrder.dateAndTimeAsc,
) -> models.PhotoList:
    return await digikam.photos(limit, offset, order, settings.ignored_roots, album)


@app.get("/api/v1/photos/{photo_id}")
async def photo(photo_id: int) -> models.PhotoFull:
    return await digikam.photo(photo_id, settings.ignored_roots)


@app.get("/api/v1/photos/{photo_id}/file", response_class=FileResponse)
async def photo_file(photo_id: int, request: Request, response: Response):
    photo_file = await digikam.photo_file(
        photo_id, settings.ignored_roots, settings.root_map
    )
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


@app.get("/api/v1/thumbs/{thumb_hash}", response_class=FileResponse)
async def thumb_file(thumb_hash: str, request: Request, response: Response):
    thumb = await digikam.thumb_by_hash(thumb_hash)
    if not thumb:
        return Response(status_code=404)

    if last_modified := thumb.last_modified:
        response.headers["Last-Modified"] = last_modified.strftime(
            HTTP_MODIFIED_DATE_FORMAT
        )
        if if_modified_since_raw := request.headers.get("If-Modified-Since"):
            if if_modified_since := datetime.strptime(
                if_modified_since_raw, HTTP_MODIFIED_DATE_FORMAT
            ):
                if last_modified >= if_modified_since:
                    return Response(status_code=304)

    if thumb.data.startswith(b"PGF"):
        # FIXME: ignored by FastAPI, probably because it's not a proper mimetype
        response.media_type = "image/pgf"

    response.body = thumb.data
    response.status_code = 200
    return response
