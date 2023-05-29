from fastapi.testclient import TestClient

from clarita import app

client = TestClient(app)


def test_photos_no_album():
    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 46,
        "results": [
            {
                "id": "35",
                "filename": "11.jpg",
                "title": "11.jpg",
                "date_and_time": "2013-07-01T00:00:00",
            },
            {
                "id": "36",
                "filename": "12.jpg",
                "title": "12.jpg",
                "date_and_time": "2013-07-11T02:00:00",
            },
            {
                "id": "37",
                "filename": "13.jpg",
                "title": "13.jpg",
                "date_and_time": "2013-07-21T04:00:00",
            },
            {
                "id": "38",
                "filename": "14.jpg",
                "title": "14.jpg",
                "date_and_time": "2013-07-31T06:00:00",
            },
            {
                "id": "39",
                "filename": "15.jpg",
                "title": "15.jpg",
                "date_and_time": "2013-08-10T08:00:00",
            },
            {
                "id": "40",
                "filename": "16.jpg",
                "title": "Dying glacier",
                "date_and_time": "2013-08-20T10:00:00",
            },
            {
                "id": "41",
                "filename": "17.jpg",
                "title": "Dying glacier",
                "date_and_time": "2013-08-30T12:00:00",
            },
            {
                "id": "42",
                "filename": "18.jpg",
                "title": "Cascada y arcoiris",
                "date_and_time": "2013-09-09T14:00:00",
            },
            {
                "id": "43",
                "filename": "19.jpg",
                "title": "19.jpg",
                "date_and_time": "2013-09-19T16:00:00",
            },
            {
                "id": "16",
                "filename": "01.jpg",
                "title": "Slope Point",
                "date_and_time": "2017-06-01T00:00:00",
            },
            {
                "id": "17",
                "filename": "02.jpg",
                "title": "02.jpg",
                "date_and_time": "2017-06-11T02:00:00",
            },
            {
                "id": "18",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2017-06-21T04:00:00",
            },
            {
                "id": "19",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2017-07-01T06:00:00",
            },
            {
                "id": "20",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2017-07-11T08:00:00",
            },
            {
                "id": "21",
                "filename": "06.jpg",
                "title": "06.jpg",
                "date_and_time": "2017-07-21T10:00:00",
            },
            {
                "id": "22",
                "filename": "07.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-07-31T12:00:00",
            },
            {
                "id": "23",
                "filename": "08.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-10T14:00:00",
            },
            {
                "id": "24",
                "filename": "09.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-20T16:00:00",
            },
            {
                "id": "25",
                "filename": "10.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-30T18:00:00",
            },
            {
                "id": "44",
                "filename": "01.jpg",
                "title": "01.jpg",
                "date_and_time": "2018-04-01T00:00:00",
            },
            {
                "id": "26",
                "filename": "02.jpg",
                "title": "Black swan event",
                "date_and_time": "2018-04-11T02:00:00",
            },
            {
                "id": "27",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2018-04-21T04:00:00",
            },
            {
                "id": "28",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2018-05-01T06:00:00",
            },
            {
                "id": "29",
                "filename": "05.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-11T08:00:00",
            },
            {
                "id": "30",
                "filename": "06.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-21T10:00:00",
            },
            {
                "id": "31",
                "filename": "07.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-31T12:00:00",
            },
            {
                "id": "32",
                "filename": "08.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-10T14:00:00",
            },
            {
                "id": "33",
                "filename": "09.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-20T16:00:00",
            },
            {
                "id": "34",
                "filename": "10.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-30T18:00:00",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
            {
                "id": "7",
                "filename": "01.jpg",
                "title": "01.jpg",
                "date_and_time": "2019-07-19T08:59:17",
            },
            {
                "id": "8",
                "filename": "02.jpg",
                "title": "02.jpg",
                "date_and_time": "2019-09-12T19:49:43",
            },
            {
                "id": "14",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-01-05T14:33:50",
            },
            {
                "id": "15",
                "filename": "09.jpg",
                "title": "09.jpg",
                "date_and_time": "2020-01-15T17:33:07",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "9",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2020-07-14T17:27:18",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "12",
                "filename": "06.jpg",
                "title": "06.jpg",
                "date_and_time": "2020-12-05T10:04:23",
            },
            {
                "id": "13",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-12-05T16:18:59",
            },
            {
                "id": "10",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2021-06-25T16:12:39",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "11",
                "filename": "05.jpg",
                "title": "Enjoying the bounty",
                "date_and_time": "2022-01-05T17:35:36",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
        ],
    }


def test_photos_with_album():
    response = client.get("/api/v1/photos?album=5")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 8,
        "results": [
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
        ],
    }


def test_photos_limit_and_offset():
    response = client.get("/api/v1/photos?limit=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": 2,
        "total": 46,
        "results": [
            {
                "id": "35",
                "filename": "11.jpg",
                "title": "11.jpg",
                "date_and_time": "2013-07-01T00:00:00",
            },
            {
                "id": "36",
                "filename": "12.jpg",
                "title": "12.jpg",
                "date_and_time": "2013-07-11T02:00:00",
            },
        ],
    }
    response = client.get("/api/v1/photos?limit=2&offset=2")
    assert response.status_code == 200
    assert response.json() == {
        "next": 4,
        "total": 46,
        "results": [
            {
                "id": "37",
                "filename": "13.jpg",
                "title": "13.jpg",
                "date_and_time": "2013-07-21T04:00:00",
            },
            {
                "id": "38",
                "filename": "14.jpg",
                "title": "14.jpg",
                "date_and_time": "2013-07-31T06:00:00",
            },
        ],
    }


def test_photos_order_title_asc():
    response = client.get("/api/v1/photos?album=5&order=title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 8,
        "results": [
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
        ],
    }


def test_photos_order_title_desc():
    response = client.get("/api/v1/photos?album=5&order=-title")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 8,
        "results": [
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
        ],
    }


def test_photos_order_date_and_time_asc():
    response = client.get("/api/v1/photos?album=5&order=date_and_time")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 8,
        "results": [
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
        ],
    }


def test_photos_order_date_and_time_desc():
    response = client.get("/api/v1/photos?album=5&order=-date_and_time")
    assert response.status_code == 200
    assert response.json() == {
        "next": None,
        "total": 8,
        "results": [
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
            },
        ],
    }
