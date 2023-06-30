from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_album_404():
    response = client.get("/api/v1/albums/12345")
    assert response.status_code == 404


def test_album_root():
    response = client.get("/api/v1/albums/1")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [],
        "date": "2023-05-29",
        "description": "",
        "id": "1",
        "thumb_hash": None,
        "title": "",
    }


def test_album_depth_1():
    response = client.get("/api/v1/albums/2")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_hash": None}
        ],
        "date": "2019-01-01",
        "description": "Caption for Album 1",
        "id": "2",
        "thumb_hash": None,
        "title": "Album 1",
    }


def test_album_depth_2():
    response = client.get("/api/v1/albums/5")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_hash": None},
            {"date": "2020-01-01", "id": "5", "title": "Album 1.1", "thumb_hash": None},
        ],
        "date": "2020-01-01",
        "description": "",
        "id": "5",
        "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
        "title": "Album 1.1",
    }


def test_album_depth_3():
    response = client.get("/api/v1/albums/7")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_hash": None},
            {"date": "2020-01-01", "id": "5", "title": "Album 1.1", "thumb_hash": None},
            {"date": "2020-01-01", "id": "7", "title": "Album 1.1.1", "thumb_hash": None},
        ],
        "date": "2020-01-01",
        "description": "",
        "id": "7",
        "thumb_hash": "88ef7a69691f6d965df146a96a155eef",
        "title": "Album 1.1.1",
    }
