import json
import os

from bot.driver import Driver
from pylol import Match


class LocalDriver(Driver):

    __version__ = "@"

    @property
    def data(self) -> dict[str, dict]:
        if not os.path.isfile(self.output_file):
            return {}

        with open(self.output_file, "r", encoding="UTF-8") as stream:
            return json.load(stream)

    def __init__(self, conf) -> None:
        super().__init__(conf)
        self.output_file = self._config.get("output_file", "storage.json")

    def find(self, _id: int):
        _m = self.data.get(str(_id))
        return None if not _m else Match.from_dict(_m)

    def find_all(self):
        return {
                int(_k): Match.from_dict(_m) \
                for _k, _m in self.data.items()
            }

    def insert(self, match: Match):
        _copy = self.data

        _copy[str(match.id)] = match.to_dict()

        with open(
            self.output_file,
            "w",
            encoding="UTF-8") as stream:
            stream.write(json.dumps(_copy))

        return True

    def drop_all(self) -> bool:
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)
        return True

def setup(config):
    return LocalDriver(config)
