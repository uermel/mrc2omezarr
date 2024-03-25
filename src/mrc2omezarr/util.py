import json
from typing import Any, Dict, Tuple


def get_protocol(path: str) -> Tuple[str, str]:
    parts = path.split("://")

    if len(parts) == 1:
        return "local", path

    return parts[0], parts[1]


def get_filesystem_args(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)
