import json

from pylol.config import CONFIG


if not CONFIG.get("output_file"):
    registered_matches = {}
else:
    with open(CONFIG["output_file"], "w+", encoding="UTF-8") as stream:
        registered_matches = json.loads(stream.read() or "{}")

def save(obj: dict):
    for match_id, match_stats in obj.items():
        registered_matches[match_id] = match_stats

    with open(
            CONFIG["output_file"],
            "w",
            encoding="UTF-8") as stream:
        stream.write(json.dumps(registered_matches))

def exists(match_id: int):
    return match_id in registered_matches
