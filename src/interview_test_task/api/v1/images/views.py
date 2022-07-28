from typing import List, Union

from fastapi import APIRouter, Query, HTTPException
from .core import get_image_from_db
from .models import Image

image_router = APIRouter(prefix="/api/v1/images")


@image_router.get(
    "",
    summary=("Получить картинку по категории."),
    status_code=200,
    responses={},
    response_model=Image,
)
async def get_image_by_category(
    category: List[str] = Query(
        default=[],
    )
) -> Union[Image, None]:
    if len(category) > 10:
        raise HTTPException(
            400, "can't handle more than 10 categories for a single request"
        )
    hit = await get_image_from_db(category)
    return hit
