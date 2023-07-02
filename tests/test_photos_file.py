from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photo_file_404():
    response = client.get("/api/v1/photos/12345/file")
    assert response.status_code == 404


def test_photo_file():
    response = client.get("/api/v1/photos/1/file")
    assert response.status_code == 200
    assert response.headers == {
        "content-type": "image/jpeg",
        "content-length": "579417",
        "last-modified": "Sat, 03 Jun 2023 07:15:59 GMT",
        "etag": "e72bd5520317869658515638214cdf2b",
    }
    assert len(response.read()) == 579417
