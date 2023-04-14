from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photos_no_album():
    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "id": "21",
                "filename": "image21.jpg",
                "title": "image21.jpg",
                "date_and_time": "2012-03-03T16:21:17",
            },
            {
                "id": "22",
                "filename": "image22.jpg",
                "title": "image22.jpg",
                "date_and_time": "2012-12-31T11:26:00",
            },
            {
                "id": "2",
                "filename": "image2.jpg",
                "title": "Title of image2",
                "date_and_time": "2014-03-15T09:41:35",
            },
            {
                "id": "19",
                "filename": "image19.jpg",
                "title": "image19.jpg",
                "date_and_time": "2014-03-23T10:12:19",
            },
            {
                "id": "20",
                "filename": "image20.jpg",
                "title": "image20.jpg",
                "date_and_time": "2014-03-23T10:49:40",
            },
            {
                "id": "1",
                "filename": "image1.jpg",
                "title": "Title of image1",
                "date_and_time": "2014-06-14T12:55:39",
            },
            {
                "id": "9",
                "filename": "image10.jpg",
                "title": "image10.jpg",
                "date_and_time": "2015-01-24T13:00:01",
            },
            {
                "id": "5",
                "filename": "image5.jpg",
                "title": "image5.jpg",
                "date_and_time": "2015-02-28T08:12:28",
            },
            {
                "id": "3",
                "filename": "image3.jpg",
                "title": "Title of image3",
                "date_and_time": "2015-03-14T12:02:51",
            },
            {
                "id": "4",
                "filename": "image4.jpg",
                "title": "image4.jpg",
                "date_and_time": "2015-03-31T11:38:23",
            },
            {
                "id": "10",
                "filename": "image11.jpg",
                "title": "image11.jpg",
                "date_and_time": "2015-06-21T15:39:41",
            },
            {
                "id": "11",
                "filename": "image12.jpg",
                "title": "image12.jpg",
                "date_and_time": "2015-07-03T18:14:56",
            },
            {
                "id": "13",
                "filename": "image13.jpg",
                "title": "image13.jpg",
                "date_and_time": "2015-07-26T09:33:53",
            },
            {
                "id": "14",
                "filename": "image14.jpg",
                "title": "image14.jpg",
                "date_and_time": "2015-07-26T12:10:21",
            },
            {
                "id": "15",
                "filename": "image15.jpg",
                "title": "image15.jpg",
                "date_and_time": "2015-08-15T11:14:52",
            },
            {
                "id": "6",
                "filename": "image6.jpg",
                "title": "image6.jpg",
                "date_and_time": "2016-02-26T11:25:58",
            },
            {
                "id": "16",
                "filename": "image16.jpg",
                "title": "image16.jpg",
                "date_and_time": "2016-02-28T02:59:03",
            },
            {
                "id": "17",
                "filename": "image17.jpg",
                "title": "image17.jpg",
                "date_and_time": "2016-03-27T04:37:17",
            },
            {
                "id": "23",
                "filename": "image23.jpg",
                "title": "image23.jpg",
                "date_and_time": "2017-11-18T17:46:07",
            },
            {
                "id": "24",
                "filename": "image24.jpg",
                "title": "image24.jpg",
                "date_and_time": "2017-11-18T17:55:31",
            },
            {
                "id": "7",
                "filename": "image7.jpg",
                "title": "image7.jpg",
                "date_and_time": "2017-12-23T07:37:34",
            },
            {
                "id": "8",
                "filename": "image8.jpg",
                "title": "image8.jpg",
                "date_and_time": "2018-02-10T06:12:47",
            },
            {
                "id": "12",
                "filename": "image9.jpg",
                "title": "image9.jpg",
                "date_and_time": "2018-11-24T06:32:45",
            },
            {
                "id": "18",
                "filename": "image18.jpg",
                "title": "image18.jpg",
                "date_and_time": "2019-08-16T17:12:00",
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
                "id": "2",
                "filename": "image2.jpg",
                "title": "Title of image2",
                "date_and_time": "2014-03-15T09:41:35",
            },
            {
                "id": "1",
                "filename": "image1.jpg",
                "title": "Title of image1",
                "date_and_time": "2014-06-14T12:55:39",
            },
            {
                "id": "3",
                "filename": "image3.jpg",
                "title": "Title of image3",
                "date_and_time": "2015-03-14T12:02:51",
            },
            {
                "id": "4",
                "filename": "image4.jpg",
                "title": "image4.jpg",
                "date_and_time": "2015-03-31T11:38:23",
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
                "date_and_time": "2012-03-03T16:21:17",
                "filename": "image21.jpg",
                "id": "21",
                "title": "image21.jpg",
            },
            {
                "date_and_time": "2012-12-31T11:26:00",
                "filename": "image22.jpg",
                "id": "22",
                "title": "image22.jpg",
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
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "title": "Title of image2",
            },
            {
                "date_and_time": "2014-03-23T10:12:19",
                "filename": "image19.jpg",
                "id": "19",
                "title": "image19.jpg",
            },
        ],
        "total": 24,
    }


def test_photos_order_title_asc():
    response = client.get("/api/v1/photos?album=2&order=title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "title": "image4.jpg",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "title": "Title of image1",
            },
            {
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "title": "Title of image2",
            },
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "title": "Title of image3",
            },
        ],
        "total": 4,
    }


def test_photos_order_title_desc():
    response = client.get("/api/v1/photos?album=2&order=-title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "title": "Title of image3",
            },
            {
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "title": "Title of image2",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "title": "Title of image1",
            },
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "title": "image4.jpg",
            },
        ],
        "total": 4,
    }


def test_photos_order_date_and_time_asc():
    response = client.get("/api/v1/photos?album=2&order=date_and_time")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "title": "Title of image2",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "title": "Title of image1",
            },
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "title": "Title of image3",
            },
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "title": "image4.jpg",
            },
        ],
        "total": 4,
    }


def test_photos_order_date_and_time_desc():
    response = client.get("/api/v1/photos?album=2&order=-date_and_time")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "results": [
            {
                "date_and_time": "2015-03-31T11:38:23",
                "filename": "image4.jpg",
                "id": "4",
                "title": "image4.jpg",
            },
            {
                "date_and_time": "2015-03-14T12:02:51",
                "filename": "image3.jpg",
                "id": "3",
                "title": "Title of image3",
            },
            {
                "date_and_time": "2014-06-14T12:55:39",
                "filename": "image1.jpg",
                "id": "1",
                "title": "Title of image1",
            },
            {
                "date_and_time": "2014-03-15T09:41:35",
                "filename": "image2.jpg",
                "id": "2",
                "title": "Title of image2",
            },
        ],
        "total": 4,
    }
