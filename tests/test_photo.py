from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photo_404():
    response = client.get("/api/v1/photo/12345")
    assert response.status_code == 404


def test_photo():
    response = client.get("/api/v1/photo/1")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [],
        "captions": [
            {"language": None, "text": "Title of image1"},
            {"language": None, "text": "Caption of image1"},
        ],
        "date_and_time": None,
        "filename": "image1.jpg",
        "id": "1",
        "image_url": "https://lorempixel.com/1200/800/",
        "name": "image1.jpg",
        "next": {
            "date_and_time": "2015-01-24T13:00:01",
            "filename": "image10.jpg",
            "id": "9",
            "name": "image10.jpg",
        },
        "prev": {
            "date_and_time": "2014-03-23T10:49:40",
            "filename": "image20.jpg",
            "id": "20",
            "name": "image20.jpg",
        },
    }
