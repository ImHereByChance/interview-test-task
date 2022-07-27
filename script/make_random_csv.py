import csv
import json
import random
import os

with open(f"{os.getcwd()}/category_names.json", "r") as f:
    category_names = json.load(f)

header = [
    "Image_URL",
    "needed_amount_of_shows",
    *[f"category_{n}" for n in range(1, 10)],
]

data = [
    [
        f"http://path_to_storage/static/image_name_{n}.png",
        random.randint(1, 100),
        *[random.choice(category_names) for _ in range(1, random.randint(1, 10) + 1)],
    ]
    for n in range(1, 1001)
]

with open("images.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
