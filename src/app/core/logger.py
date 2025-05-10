# src/app/core/logger.py

import logging
import logging.config
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s | %(message)s",
            "use_colors": None,
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "app": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False
        }
    },
    "root": {
        "handlers": ["default"],
        "level": "INFO"
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")
