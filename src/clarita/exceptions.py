class DoesNotExist(Exception):
    """A record does not exist in DB"""

    pass


class InvalidResult(Exception):
    """A DB query didn't work as it should"""

    pass
