import json
from typing import Union, Any


def load_json(file_path: str) -> Union[dict[Any, Any], list[Any]]:
    with open(file_path) as f:
        return json.load(f)


def write_json(file_path: str, data: Union[dict[Any, Any], list[Any]]) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f)