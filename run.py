import os
import json
from writer import write_json
from rkrattsbaser import get_year, get_newer_items
from utils import get_latest_update, sort

RESET = False
data = []

if RESET or not os.path.exists("data"):
    os.makedirs("data", exist_ok=True)

    for i in range(1686, 2025 + 1):
        print(f"Fetching {i}...")
        year_data = get_year(i)

        if year_data:
            write_json(year_data, f"data/{i}.json")
            data.extend(year_data)

else:
    with open("data/all.json", "r") as file:
        data = json.load(file)

    latest_update = get_latest_update(data)
    new_data = get_newer_items(latest_update)
    new_data = sort(new_data)

    new_beteckning = [item["_source"]["beteckning"] for item in new_data]

    to_remove = []

    for i, item in enumerate(data):
        if item["_source"]["beteckning"] in new_beteckning:
            to_remove.append(i)

    for i in sorted(to_remove):
        data.pop(i)

    data.extend(new_data)

data = sort(data)
write_json(data, "data/all.json")
