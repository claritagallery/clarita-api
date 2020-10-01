from digikam import DigikamSQLite
from fastapi import FastAPI
from models.albums import Album
from models.photos import Photo


app = FastAPI()
digikam = DigikamSQLite("/home/fidel/digikam_data/")


@app.get("/api/v1/albums")
async def albums():
    albums = await digikam.albums()
    return {"albums": albums}


@app.get("/api/v1/album/{album_id}")
async def album(album_id: int):
    return Album(id="1", name="Album 1")


@app.get("/api/v1/album/{album_id}/photo/{photo_id}")
async def photo_in_album(album_id: int, photo_id: int):
    return Photo(id="1", name="Photo 1", image_url="https://lorempixel.com/400/300/")


@app.get("/api/v1/photo/{photo_id}")
async def photo(photo_id: int):
    return Photo(id="1", name="Photo 1", image_url="https://lorempixel.com/400/300/")
