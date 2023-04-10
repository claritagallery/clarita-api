import logging.config

from .config import settings


def setup_logging():
    """

    .env should already have been loaded before calling setup_logging()

    """
    handlers = {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    }
    if logfile := settings.error_log_filename:
        handlers["logfile"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": logfile,
            "formatter": "default",
            "backupCount": "2",
        }

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
            "handlers": handlers,
            "loggers": {
                "clarita": {
                    "level": settings.loglevel_clarita,
                    "handlers": list(handlers.keys()),
                    "propagate": False,
                },
            },
            "root": {
                "level": settings.loglevel_root,
                "handlers": list(handlers.keys()),
            },
        }
    )
