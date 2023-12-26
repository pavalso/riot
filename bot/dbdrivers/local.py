import json
import os

from typing import Any

from bot.driver import Driver


class LocalDriver(Driver):

    __version__ = "@"

    @property
    def data(self) -> dict[str, Any]:
        if not os.path.isfile(self.output_file):
            return {}

        with open(self.output_file, "r", encoding="UTF-8") as stream:
            return json.load(stream)

    def __init__(self, conf: dict) -> None:
        super().__init__(conf)

        self.output_file = self._config.get("output_file") or "storage.json"

    def find(self, _id: int):
        return self.data.get(str(_id))

    def find_all(self):
        return self.data

    def insert(self, _id: int, _data: dict[str, Any]):
        _copy = self.data

        _copy[str(_id)] = _data

        with open(
            self.output_file,
            "w",
            encoding="UTF-8") as stream:
            stream.write(json.dumps(_copy))

        return True

def setup(config: dict):
    return LocalDriver(config)
