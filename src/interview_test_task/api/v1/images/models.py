from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    id: int
    url: str
    needed_amount_of_shows: int
    hit_category: str
