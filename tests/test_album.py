from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_album_404():
    response = client.get("/api/v1/album/12345")
    assert response.status_code == 404


def test_album_root():
    response = client.get("/api/v1/album/1")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [],
        "date": "2019-08-16",
        "description": "",
        "id": "1",
        "name": "",
    }


def test_album_depth_1():
    response = client.get("/api/v1/album/2")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [{"date": "2019-01-01", "id": "2", "name": "Album1"}],
        "date": "2019-01-01",
        "description": "Caption for Album1",
        "id": "2",
        "name": "Album1",
    }


def test_album_depth_2():
    response = client.get("/api/v1/album/5")
    assert response.status_code == 200
    assert response.json() == {
        "breadcrumbs": [
            {"date": "2019-01-01", "id": "2", "name": "Album1"},
            {"date": "2019-04-04", "id": "5", "name": "Album1.1"},
        ],
        "date": "2019-04-04",
        "description": "",
        "id": "5",
        "name": "Album1.1",
    }
