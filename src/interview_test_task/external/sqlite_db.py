import aiosqlite
from ..settings import settings
from loguru import logger


async def test_db_connection():
    try:
        async with aiosqlite.connect(settings.SQLITE_DB_PATH) as db:
            await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
            logger.info("db connection is ok")
    except Exception as e:
        logger.error("an error occurred while testing db connection")
        raise e
