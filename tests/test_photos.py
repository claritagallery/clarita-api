from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photos_no_album():
    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    assert response.json() == {
        "next": 20,
        "results": [
            {
                "date_and_time": "2019-08-16T17:12:00",
                "filename": "image18.jpg",
                "id": "18",
                "name": "image18.jpg",
            },
            {
                "date_and_time": "2018-11-24T06:32:45",
                "filename": "image9.jpg",
                "id": "12",
                "name": "image9.jpg",
            },
            {
                "date_and_time": "2018-02-10T06:12:47",
                "filename": "image8.jpg",
                "id": "8",
                "name": "image8.jpg",
            },
            {
                "date_and_time": "2017-12-23T07:37:34",
                "filename": "image7.jpg",
                "id": "7",
                "name": "image7.jpg",
            },
            {
                "date_and_time": "2017-11-18T17:55:31",
                "filename": "image24.jpg",
                "id": "24",
                "name": "image24.jpg",
            },
            {
                "date_and_time": "2017-11-18T17:46:07",
                "filename": "image23.jpg",
                "id": "23",
                "name": "image23.jpg",
            },
            {
                "date_and_time": "2016-03-27T04:37:17",
                "filename": "image17.jpg",
                "id": "17",
                "name": "image17.jpg",
            },
            {
                "date_and_time": "2016-02-28T02:59:03",
                "filename": "image16.jpg",
                "id": "16",
                "name": "image16.jpg",
            },
            {
                "date_and_time": "2016-02-26T11:25:58",
                "filename": "image6.jpg",
                "id": "6",
                "name": "image6.jpg",
            },
            {
                "date_and_time": "2015-08-15T11:14:52",
                "filename": "image15.jpg",
                "id": "15",
                "name": "image15.jpg",
            },
            {
                "date_and_time": "2015-07-26T12:10:21",
                "filename": "image14.jpg",
                "id": "14",
                "name": "image14.jpg",
            },
            {
                "date_and_time": "2015-07-26T09:33:53",
                "filename": "image13.jpg",
                "id": "13",
                "name": "image13.jpg",
            },
            {
                "date_and_time": "2015-07-03T18:14:56",
                "filename": "image12.jpg",
                "id": "11",
                "name": "image12.jpg",
            },
            {
                "date_and_time": "2015-06-21T15:39:41",
                "filename": "image11.jpg",
                "id": "10",
                "name": "image11.jpg",
            },
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "name": "image4.jpg",
            },
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "name": "image3.jpg",
            },
            {
                "date_and_time": "2015-02-28T08:12:28",
                "filename": "image5.jpg",
                "id": "5",
                "name": "image5.jpg",
            },
            {
                "date_and_time": "2015-01-24T13:00:01",
                "filename": "image10.jpg",
                "id": "9",
                "name": "image10.jpg",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "name": "image1.jpg",
            },
            {
                "date_and_time": "2014-03-23T10:49:40",
                "filename": "image20.jpg",
                "id": "20",
                "name": "image20.jpg",
            },
        ],
        "total": 24,
    }


def test_photos_with_album():
    response = client.get("/api/v1/photos?album=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "name": "image4.jpg",
            },
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "name": "image3.jpg",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "name": "image1.jpg",
            },
            {
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "name": "image2.jpg",
            },
        ],
        "total": 4,
    }


def test_photos_limit_and_offset():
    response = client.get("/api/v1/photos?limit=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": 2,
        "results": [
            {
                "date_and_time": "2019-08-16T17:12:00",
                "filename": "image18.jpg",
                "id": "18",
                "name": "image18.jpg",
            },
            {
                "date_and_time": "2018-11-24T06:32:45",
                "filename": "image9.jpg",
                "id": "12",
                "name": "image9.jpg",
            },
        ],
        "total": 24,
    }
    response = client.get("/api/v1/photos?limit=2&offset=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": 4,
        "results": [
            {
                "date_and_time": "2018-02-10T06:12:47",
                "filename": "image8.jpg",
                "id": "8",
                "name": "image8.jpg",
            },
            {
                "date_and_time": "2017-12-23T07:37:34",
                "filename": "image7.jpg",
                "id": "7",
                "name": "image7.jpg",
            },
        ],
        "total": 24,
    }
