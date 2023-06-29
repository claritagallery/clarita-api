from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photo_404():
    response = client.get("/api/v1/photos/12345")
    assert response.status_code == 404


def test_photo():
    response = client.get("/api/v1/photos/1")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [],
        "date_and_time": "2021-10-09T16:24:01",
        "description": "",
        "filename": "01.jpg",
        "id": "1",
        "image_url": "/api/v1/photos/1/file",
        "next": {
            "id": "2",
            "filename": "02.jpg",
            "title": "Icecream!",
            "date_and_time": "2021-10-09T16:36:17",
            "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
        },
        "prev": {
            "id": "10",
            "filename": "04.jpg",
            "title": "04.jpg",
            "date_and_time": "2021-06-25T16:12:39",
            "thumb_hash": "88ef7a69691f6d965df146a96a155eef",
        },
        "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
        "title": "Icecream!",
    }
