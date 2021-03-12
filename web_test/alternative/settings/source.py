import os
from_env = os.getenv


def from_json(file: str):
    def source(key, default=None):
        try:
            import json
            parsed = json.load(open(file))
        except Exception:
            return default
        else:
            return parsed.get(key)

    return source
