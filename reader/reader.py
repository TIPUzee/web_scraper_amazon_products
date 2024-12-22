import json


def load_json(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)
