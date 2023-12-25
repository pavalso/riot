import json
import os

from typing import Any

from bot.driver import Driver


class LocalDriver(Driver):

    __version__ = "@"

    def __init__(self, conf: dict) -> None:
        super().__init__(conf)

        self.output_file = self._config.get("output_file") or "storage.json"

        if not self.output_file or not os.path.isfile(self.output_file):
            self.data = {}
        else:
            with open(self.output_file, "r", encoding="UTF-8") as stream:
                self.data = json.load(stream)
                print(self.data.keys())

    def find(self, _id: int):
        return self.data.get(str(_id))

    def find_all(self):
        return self.data

    def insert(self, _id: int, _data: dict[str, Any]):
        self.data[str(_id)] = _data

        with open(
            self.output_file,
            "w",
            encoding="UTF-8") as stream:
            stream.write(json.dumps(self.data))

def setup(config: dict):
    return LocalDriver(config)
