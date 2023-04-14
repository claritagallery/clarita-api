import enum


class AlbumOrder(enum.Enum):
    titleAsc = "title"
    titleDesc = "-title"
    dateAsc = "date"
    dateDesc = "-date"


class PhotoOrder(enum.Enum):
    titleAsc = "title"
    titleDesc = "-title"
    dateAndTimeAsc = "date_and_time"
    dateAndTimeDesc = "-date_and_time"
