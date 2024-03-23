import json
from os import listdir


def load_json(path:str):
    existing_json = list(filter(lambda file: not file.startswith("_") and file.endswith(".json") ,listdir(path)))
    outputs = []
    for filename in existing_json:
        data = json.load(open(f"{path}/{filename}"))
        is_array = isinstance(data, list)
        if is_array:
            outputs.append(f"{path}/{filename}")
    return outputs
