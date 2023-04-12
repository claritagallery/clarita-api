import enum


class AlbumOrder(enum.Enum):
    titleAsc = "title"
    titleDesc = "-title"
    dateAsc = "date"
    dateDesc = "-date"
