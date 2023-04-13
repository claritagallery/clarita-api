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
        "description": "Caption of image1",
        "date_and_time": "2014-06-14T12:55:39",
        "filename": "image1.jpg",
        "id": "1",
        "image_url": "/api/v1/photos/1/file",
        "next": {
            "date_and_time": "2015-01-24T13:00:01",
            "filename": "image10.jpg",
            "id": "9",
            "title": "image10.jpg",
        },
        "prev": {
            "date_and_time": "2014-03-23T10:49:40",
            "filename": "image20.jpg",
            "id": "20",
            "title": "image20.jpg",
        },
        "title": "Title of image1",
    }
