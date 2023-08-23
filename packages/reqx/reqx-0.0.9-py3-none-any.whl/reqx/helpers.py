from pathlib import Path
import orjson


def dump_json(data: dict | list, filename: str = 'tmp.json'):
    Path(filename).write_bytes(orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS))
