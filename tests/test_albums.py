from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_albums_root():
    response = client.get("/api/v1/albums")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-08-16", "id": "1", "title": ""},
            {"date": "2019-01-01", "id": "2", "title": "Album1"},
            {"date": "2019-02-02", "id": "3", "title": "Album2"},
            {"date": "2019-03-03", "id": "4", "title": "Album3"},
        ],
        "total": 4,
    }


def test_albums_for_parent_depth_1():
    response = client.get("/api/v1/albums?parent=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-04-04", "id": "5", "title": "Album1.1"},
            {"date": "2019-05-05", "id": "6", "title": "Album1.2"},
        ],
        "total": 2,
    }


def test_albums_for_parent_depth_2():
    response = client.get("/api/v1/albums?parent=5")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [],
        "total": 0,
    }


def test_albums_order_title_asc():
    response = client.get("/api/v1/albums?order=title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-08-16", "id": "1", "title": ""},
            {"date": "2019-01-01", "id": "2", "title": "Album1"},
            {"date": "2019-02-02", "id": "3", "title": "Album2"},
            {"date": "2019-03-03", "id": "4", "title": "Album3"},
        ],
        "total": 4,
    }


def test_albums_order_title_desc():
    response = client.get("/api/v1/albums?order=-title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-03-03", "id": "4", "title": "Album3"},
            {"date": "2019-02-02", "id": "3", "title": "Album2"},
            {"date": "2019-01-01", "id": "2", "title": "Album1"},
            {"date": "2019-08-16", "id": "1", "title": ""},
        ],
        "total": 4,
    }


def test_albums_order_date_asc():
    response = client.get("/api/v1/albums?order=date")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-01-01", "id": "2", "title": "Album1"},
            {"date": "2019-02-02", "id": "3", "title": "Album2"},
            {"date": "2019-03-03", "id": "4", "title": "Album3"},
            {"date": "2019-08-16", "id": "1", "title": ""},
        ],
        "total": 4,
    }


def test_albums_order_date_desc():
    response = client.get("/api/v1/albums?order=-date")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-08-16", "id": "1", "title": ""},
            {"date": "2019-03-03", "id": "4", "title": "Album3"},
            {"date": "2019-02-02", "id": "3", "title": "Album2"},
            {"date": "2019-01-01", "id": "2", "title": "Album1"},
        ],
        "total": 4,
    }
