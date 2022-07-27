import asyncio
import aiosqlite
from typing import Dict, List, Literal, Set, Tuple, Union
from pathlib import Path

path_to_db = Path(__file__).parent.parent / "db"

# custom types for db entities to make it a bit more clear

# id of an image, url, needed amount of shows for an image
Image = Tuple[int, str, int]
# id of a category, name of a category
Category = List[Tuple[int, str]]
# id of an image, id of a Category (junction table for many-to-many relationship)
ImageCategory = List[Tuple[int, int]]
# structure of the dict to pas to insert_data() function
DataFromCsv = Dict[
    Literal[
        "images",
        "categories",
        "image_categories",
    ],
    Union[List[Image], List[Category], List[ImageCategory]],
]


def get_data_from_csv(csv_file_path: str) -> DataFromCsv:
    with open(csv_file_path, "r") as f:
        file_content = f.read()
    parsed_file_content = [row.split(",") for row in file_content.split("\n") if row]

    images, categories, image_categories = [], [], []
    categories_set: Set[str] = set()
    for i, row in enumerate(parsed_file_content[1:], start=1):  # exclude header
        images.append((i, row[0], int(row[1])))
        for category in row[3:]:
            categories_set.add(category)
    categories = list(enumerate(categories_set, start=1))
    categories_dict = {cat: cat_id for cat_id, cat in categories}
    for image_id, row in enumerate(parsed_file_content[1:], start=1):
        for image_category in row[2:]:
            image_categories.append((image_id, categories_dict[image_category]))

    return {
        "images": images,
        "categories": categories,
        "image_categories": image_categories,
    }


async def insert_data(data_from_csv: DataFromCsv):
    async with aiosqlite.connect(str(path_to_db)) as db:
        await db.executemany(
            "INSERT INTO image ('id', 'url', 'needed_amount_of_shows') values ($1, $2, $3)",
            data_from_csv["images"],
        )
        await db.executemany(
            "INSERT INTO category ('id', 'name') values ($1, $2)",
            data_from_csv["categories"],
        )
        await db.executemany(
            "INSERT INTO image_category ('image_id', 'category_id') values ($1, $2)",
            data_from_csv["image_categories"],
        )
        await db.commit()


if __name__ == "__main__":
    data = get_data_from_csv(str(Path(__file__).parent / "images.csv"))
    asyncio.run(insert_data(data))
