import logging
import os

DEFAULT_ERROR_LOG = "error.log"


def setup_logging():
    """

    .env should already have been loaded before calling setup_logging()

    """
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d "
                    "%(levelname)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "simple": {
                    "format": "%(message)s",
                },
            },
            "handlers": {
                "logfile": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "filename": os.getenv("ERROR_LOG_FILENAME", DEFAULT_ERROR_LOG),
                    "formatter": "default",
                    "backupCount": 2,
                },
                "stdout": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "clarita": {
                    "level": "DEBUG",
                    "handlers": ["stdout"],
                },
            },
            "root": {"level": "INFO", "handlers": ["logfile", "stdout"]},
        }
    )
