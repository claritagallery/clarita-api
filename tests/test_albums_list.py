from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_albums_root():
    response = client.get("/api/v1/albums")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2023-05-29", "id": "1", "title": "", "thumb_id": None},
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_id": None},
            {"date": "2019-02-02", "id": "3", "title": "Album 2", "thumb_id": None},
            {"date": "2019-03-03", "id": "4", "title": "Album 3", "thumb_id": "25"},
            {"date": "2019-04-04", "id": "10", "title": "Album 4", "thumb_id": None},
        ],
        "total": 5,
    }


def test_albums_for_parent_depth_1():
    response = client.get("/api/v1/albums?parent=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2020-01-01", "id": "5", "title": "Album 1.1", "thumb_id": "2"},
            {"date": "2021-01-01", "id": "6", "title": "Album 1.2", "thumb_id": None},
        ],
        "total": 2,
    }


def test_albums_for_parent_depth_2():
    response = client.get("/api/v1/albums?parent=5")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2020-01-01", "id": "7", "title": "Album 1.1.1", "thumb_id": "10"},
            {"date": "2020-02-02", "id": "8", "title": "Album 1.1.2", "thumb_id": None},
            {"date": "2020-03-03", "id": "9", "title": "Album 1.1.3", "thumb_id": None},
        ],
        "total": 3,
    }


def test_albums_for_parent_with_no_children():
    response = client.get("/api/v1/albums?parent=7")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [],
        "total": 0,
    }


def test_albums_for_non_existing_parent():
    response = client.get("/api/v1/albums?parent=424242")
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
            {"date": "2023-05-29", "id": "1", "title": "", "thumb_id": None},
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_id": None},
            {"date": "2019-02-02", "id": "3", "title": "Album 2", "thumb_id": None},
            {"date": "2019-03-03", "id": "4", "title": "Album 3", "thumb_id": "25"},
            {"date": "2019-04-04", "id": "10", "title": "Album 4", "thumb_id": None},
        ],
        "total": 5,
    }


def test_albums_order_title_desc():
    response = client.get("/api/v1/albums?order=-title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-04-04", "id": "10", "title": "Album 4", "thumb_id": None},
            {"date": "2019-03-03", "id": "4", "title": "Album 3", "thumb_id": "25"},
            {"date": "2019-02-02", "id": "3", "title": "Album 2", "thumb_id": None},
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_id": None},
            {"date": "2023-05-29", "id": "1", "title": "", "thumb_id": None},
        ],
        "total": 5,
    }


def test_albums_order_date_asc():
    response = client.get("/api/v1/albums?order=date")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_id": None},
            {"date": "2019-02-02", "id": "3", "title": "Album 2", "thumb_id": None},
            {"date": "2019-03-03", "id": "4", "title": "Album 3", "thumb_id": "25"},
            {"date": "2019-04-04", "id": "10", "title": "Album 4", "thumb_id": None},
            {"date": "2023-05-29", "id": "1", "title": "", "thumb_id": None},
        ],
        "total": 5,
    }


def test_albums_order_date_desc():
    response = client.get("/api/v1/albums?order=-date")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {"date": "2023-05-29", "id": "1", "title": "", "thumb_id": None},
            {"date": "2019-04-04", "id": "10", "title": "Album 4", "thumb_id": None},
            {"date": "2019-03-03", "id": "4", "title": "Album 3", "thumb_id": "25"},
            {"date": "2019-02-02", "id": "3", "title": "Album 2", "thumb_id": None},
            {"date": "2019-01-01", "id": "2", "title": "Album 1", "thumb_id": None},
        ],
        "total": 5,
    }
