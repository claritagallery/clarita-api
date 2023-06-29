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
                "thumb_hash": "cfbe4f47262da4b076def74bff2d6d70",
            },
            {
                "id": "36",
                "filename": "12.jpg",
                "title": "12.jpg",
                "date_and_time": "2013-07-11T02:00:00",
                "thumb_hash": "6e5d59497652540170a059976d5b3e93",
            },
            {
                "id": "37",
                "filename": "13.jpg",
                "title": "13.jpg",
                "date_and_time": "2013-07-21T04:00:00",
                "thumb_hash": "90b9484ea4d1f581b2b51957e6ab270d",
            },
            {
                "id": "38",
                "filename": "14.jpg",
                "title": "14.jpg",
                "date_and_time": "2013-07-31T06:00:00",
                "thumb_hash": "1ee5462e76a81ec77489e688495c1544",
            },
            {
                "id": "39",
                "filename": "15.jpg",
                "title": "15.jpg",
                "date_and_time": "2013-08-10T08:00:00",
                "thumb_hash": "33235b07b1f9b9d7a13ae583e6fb2498",
            },
            {
                "id": "40",
                "filename": "16.jpg",
                "title": "Dying glacier",
                "date_and_time": "2013-08-20T10:00:00",
                "thumb_hash": "ebad7402aef851da33219e9f1a3e47a1",
            },
            {
                "id": "41",
                "filename": "17.jpg",
                "title": "Dying glacier",
                "date_and_time": "2013-08-30T12:00:00",
                "thumb_hash": "08bd1358a2b27a8e8b2580f7f9d95163",
            },
            {
                "id": "42",
                "filename": "18.jpg",
                "title": "Cascada y arcoiris",
                "date_and_time": "2013-09-09T14:00:00",
                "thumb_hash": "8e2fd7d5972aacc586b6f8d0980af04e",
            },
            {
                "id": "43",
                "filename": "19.jpg",
                "title": "19.jpg",
                "date_and_time": "2013-09-19T16:00:00",
                "thumb_hash": "fdb533dc009999e6a6180d33b1996a6f",
            },
            {
                "id": "16",
                "filename": "01.jpg",
                "title": "Slope Point",
                "date_and_time": "2017-06-01T00:00:00",
                "thumb_hash": "960a6eff870adba78f304f67f0f9aba5",
            },
            {
                "id": "17",
                "filename": "02.jpg",
                "title": "02.jpg",
                "date_and_time": "2017-06-11T02:00:00",
                "thumb_hash": "02908f19bef987f9c2f0d5b3b2825abf",
            },
            {
                "id": "18",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2017-06-21T04:00:00",
                "thumb_hash": "bbb06679d920e08504053de912763f46",
            },
            {
                "id": "19",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2017-07-01T06:00:00",
                "thumb_hash": "18686b598cbb0642e76b6c34b5c9a214",
            },
            {
                "id": "20",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2017-07-11T08:00:00",
                "thumb_hash": "702b54a0b038e32d3718b01d14680c9f",
            },
            {
                "id": "21",
                "filename": "06.jpg",
                "title": "06.jpg",
                "date_and_time": "2017-07-21T10:00:00",
                "thumb_hash": "d1e60f87fca31a3951849c4ab6f91fde",
            },
            {
                "id": "22",
                "filename": "07.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-07-31T12:00:00",
                "thumb_hash": "a3e1091611275f09940b990725d88732",
            },
            {
                "id": "23",
                "filename": "08.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-10T14:00:00",
                "thumb_hash": "f6a3c2239b5a3d56019b3e3aee616289",
            },
            {
                "id": "24",
                "filename": "09.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-20T16:00:00",
                "thumb_hash": "1203145bfeb89a8fee73e9119dec13b2",
            },
            {
                "id": "25",
                "filename": "10.jpg",
                "title": "Camino Inca",
                "date_and_time": "2017-08-30T18:00:00",
                "thumb_hash": "eeb4f6bcbcc77fad1e43d0da6dabdc09",
            },
            {
                "id": "44",
                "filename": "01.jpg",
                "title": "01.jpg",
                "date_and_time": "2018-04-01T00:00:00",
                "thumb_hash": "1eebda921e8823abd40f9ca32b380774",
            },
            {
                "id": "26",
                "filename": "02.jpg",
                "title": "Black swan event",
                "date_and_time": "2018-04-11T02:00:00",
                "thumb_hash": "6b4ade1a3c8797eead77c8e8eeb9c56d",
            },
            {
                "id": "27",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2018-04-21T04:00:00",
                "thumb_hash": "4d5e4cbd5f9f41ec8524a7d29c540203",
            },
            {
                "id": "28",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2018-05-01T06:00:00",
                "thumb_hash": "efffed2c52389198083f6eb2ddd48181",
            },
            {
                "id": "29",
                "filename": "05.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-11T08:00:00",
                "thumb_hash": "1701c77aceedf31401dc26cb0b103468",
            },
            {
                "id": "30",
                "filename": "06.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-21T10:00:00",
                "thumb_hash": "0d4b11b9a30ab3c8d13c51079d3dc52d",
            },
            {
                "id": "31",
                "filename": "07.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-05-31T12:00:00",
                "thumb_hash": "15135e65a222413e0e8a0a9507573b98",
            },
            {
                "id": "32",
                "filename": "08.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-10T14:00:00",
                "thumb_hash": "cd6cc862b3e7f57c5339e385f84d0d56",
            },
            {
                "id": "33",
                "filename": "09.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-20T16:00:00",
                "thumb_hash": "5a812a619f225076d125c76b685b88a7",
            },
            {
                "id": "34",
                "filename": "10.jpg",
                "title": "Milford Sound",
                "date_and_time": "2018-06-30T18:00:00",
                "thumb_hash": "b16ce82cf320841fa7dd9a90c75b604f",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
            {
                "id": "7",
                "filename": "01.jpg",
                "title": "01.jpg",
                "date_and_time": "2019-07-19T08:59:17",
                "thumb_hash": "bb1ca471afb42a923c413ea0eec8e271",
            },
            {
                "id": "8",
                "filename": "02.jpg",
                "title": "02.jpg",
                "date_and_time": "2019-09-12T19:49:43",
                "thumb_hash": "d862b59c5ce0aa77eb9c0858808fb33a",
            },
            {
                "id": "14",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-01-05T14:33:50",
                "thumb_hash": "c8f5093a15004892317b8156b85e1e9a",
            },
            {
                "id": "15",
                "filename": "09.jpg",
                "title": "09.jpg",
                "date_and_time": "2020-01-15T17:33:07",
                "thumb_hash": "374339784ccc5ae1d6ddb08c1e2e8b22",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "9",
                "filename": "03.jpg",
                "title": "03.jpg",
                "date_and_time": "2020-07-14T17:27:18",
                "thumb_hash": "13b059d39e12dc3f62cafa05ffd85ab7",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "12",
                "filename": "06.jpg",
                "title": "06.jpg",
                "date_and_time": "2020-12-05T10:04:23",
                "thumb_hash": "89a0daa71072f9df9b1bfda591a36dd3",
            },
            {
                "id": "13",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-12-05T16:18:59",
                "thumb_hash": "3467c5e6cc2337a5bd208d16844cd9a1",
            },
            {
                "id": "10",
                "filename": "04.jpg",
                "title": "04.jpg",
                "date_and_time": "2021-06-25T16:12:39",
                "thumb_hash": "88ef7a69691f6d965df146a96a155eef",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "11",
                "filename": "05.jpg",
                "title": "Enjoying the bounty",
                "date_and_time": "2022-01-05T17:35:36",
                "thumb_hash": "3a07dcafa5ca53f78601d831feade54b",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
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
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
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
                "thumb_hash": "cfbe4f47262da4b076def74bff2d6d70",
            },
            {
                "id": "36",
                "filename": "12.jpg",
                "title": "12.jpg",
                "date_and_time": "2013-07-11T02:00:00",
                "thumb_hash": "6e5d59497652540170a059976d5b3e93",
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
                "thumb_hash": "90b9484ea4d1f581b2b51957e6ab270d",
            },
            {
                "id": "38",
                "filename": "14.jpg",
                "title": "14.jpg",
                "date_and_time": "2013-07-31T06:00:00",
                "thumb_hash": "1ee5462e76a81ec77489e688495c1544",
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
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
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
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
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
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "6",
                "filename": "04.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:54:15",
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
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
                "thumb_hash": "8be03f39750e220467d8d4aa45b05e74",
            },
            {
                "id": "3",
                "filename": "03.jpg",
                "title": "Traje de flamenca",
                "date_and_time": "2023-04-23T15:44:11",
                "thumb_hash": "f1e727c64dff721d6ed437cf6976281c",
            },
            {
                "id": "4",
                "filename": "05.jpg",
                "title": "05.jpg",
                "date_and_time": "2022-07-06T12:53:41",
                "thumb_hash": "f3c3889994b3b63bb8ed5c84fec91e2b",
            },
            {
                "id": "2",
                "filename": "02.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:36:17",
                "thumb_hash": "99c7ca6f440e843be08b5328223c9f21",
            },
            {
                "id": "1",
                "filename": "01.jpg",
                "title": "Icecream!",
                "date_and_time": "2021-10-09T16:24:01",
                "thumb_hash": "9fa1106d25b7701e4b0b000804924dca",
            },
            {
                "id": "45",
                "filename": "07.jpg",
                "title": "07.jpg",
                "date_and_time": "2020-09-05T18:18:12",
                "thumb_hash": "575eb63bcaed0d218a934aaddfb1fa7c",
            },
            {
                "id": "46",
                "filename": "08.jpg",
                "title": "08.jpg",
                "date_and_time": "2020-03-08T12:26:19",
                "thumb_hash": "9ae27d36808d1f81cd9b5df275a6b578",
            },
            {
                "id": "5",
                "filename": "06.jpg",
                "title": "Natural mohawk",
                "date_and_time": "2019-04-25T13:38:52",
                "thumb_hash": "df63f0a1bc80460e0392aba176a771dc",
            },
        ],
    }
