import json
import os
from datasets import Dataset
from dotenv import load_dotenv

from lib.load_json import load_json
load_dotenv()

class DatasetBuilder:
    def __init__(self, keys: list[str]):
        self.keys = keys
        rows = {}
        for key in keys:
            rows[key] = []
        self.rows = rows

    def add_row(self, row:dict):
        for key in self.keys:
            self.rows[key].append(row[key])

    def to_dataset(self):
        return Dataset.from_dict(self.rows)

def run():
    target_json = load_json("datasets")
    for json_file in target_json:
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        data = json.load(open(json_file))
        existing_keys: list[str] = []
        for i, d in enumerate(data):
            keys = list(d.keys())
            for key in keys:
                if key not in existing_keys:
                    existing_keys.append(key)
        builder = DatasetBuilder(existing_keys)
        for d in data:
            builder.add_row(d)
        dataset = builder.to_dataset()
        hfuser = os.getenv("HUGGING_FACE_USER_ID")
        hftoken = os.getenv("HUGGING_FACE_TOKEN")
        if not hfuser or not hftoken:
            raise Exception("Hugging Face credentials not found")
            
        dataset.push_to_hub(f"{hfuser}/{base_name}",token=hftoken)

run()
