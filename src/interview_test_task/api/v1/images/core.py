from typing import List, Union

import aiosqlite
from .models import Image

from ....settings import settings


async def get_image_from_db(categories: List[str]) -> Union[Image, None]:
    # NOTE: неатомарные транзакции подобные этой могут привести к аномалиям
    # при конкурентном выполнении. Так как здесь используется sqlitе3
    # одним единственным инстансом приложения, можно не думать об уровнях изоляции
    # транзакций или блокировках (на проде это нужно учитывать).
    placeholders = ", ".join(f"${i}" for i in range(1, len(categories) + 1))
    image_by_category_query = f"""
        SELECT i.*, c.name
        FROM image i
        JOIN image_category ic ON i.id = ic.image_id 
        JOIN category c ON ic.category_id = c.id
        WHERE c.name IN ({placeholders}) AND i.needed_amount_of_shows > 0
        ORDER BY random()
        LIMIT 1
    """
    random_image_query = """
        SELECT i.*, c.name
        FROM image i
        JOIN image_category ic ON i.id = ic.image_id 
        JOIN category c ON ic.category_id = c.id
        WHERE i.needed_amount_of_shows > 0
        ORDER BY random()
        LIMIT 1
    """
    update_query = """
        UPDATE image
        SET needed_amount_of_shows = needed_amount_of_shows - 1
        WHERE image.id = $1
    """
    async with aiosqlite.connect(settings.SQLITE_DB_PATH) as db:
        cursor = await db.execute(
            image_by_category_query if categories else random_image_query,
            categories,
        )
        result = await cursor.fetchone()
        if not result:
            return None
        image_as_model = Image(
            id=result[0],
            url=result[1],
            needed_amount_of_shows=result[2],
            hit_category=result[3],
        )
        await db.execute(update_query, [image_as_model.id])
        await db.commit()
        return image_as_model
