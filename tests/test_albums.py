from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_albums_root():
    response = client.get("/api/v1/albums")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-08-16", "id": "1", "name": ""},
            {"date": "2019-03-03", "id": "4", "name": "Album3"},
            {"date": "2019-02-02", "id": "3", "name": "Album2"},
            {"date": "2019-01-01", "id": "2", "name": "Album1"},
        ],
        "total": 4,
    }


def test_albums_for_parent_depth_1():
    response = client.get("/api/v1/albums?parent=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-05-05", "id": "6", "name": "Album1.2"},
            {"date": "2019-04-04", "id": "5", "name": "Album1.1"},
            {"date": "2019-01-01", "id": "2", "name": ""},
        ],
        "total": 3,
    }


def test_albums_for_parent_depth_2():
    response = client.get("/api/v1/albums?parent=5")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [],
        "total": 0,
    }
