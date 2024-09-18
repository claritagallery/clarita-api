from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_thumb_file_404():
    response = client.get("/api/v1/photos/12345/thumb")
    assert response.status_code == 404


def test_thumb_file():
    response = client.get("/api/v1/photos/1/thumb")
    assert response.status_code == 200
    assert response.headers == {
        "content-type": "image/jpeg",
        "content-length": "11270",
        "last-modified": "Tue, 10 Sep 2024 13:27:42 GMT",
        "etag": '"48efb3b9821fb2e1ca68b67db1cd9986"',
    }
    assert len(response.read()) == 11270
