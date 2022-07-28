import os
import sys

from fastapi import FastAPI
from loguru import logger

from .api.v1.images.views import image_router
from .external.sqlite_db import test_db_connection

app = FastAPI(
    title="Interview test task",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)

logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",
        }
    ]
}


def create_app():
    logger.configure(**logger_config)
    app.include_router(image_router)
    app.add_event_handler("startup", test_db_connection)
    return app
