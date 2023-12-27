import json
import os

from typing import Any

from bot.driver import Driver


class MemoryDriver(Driver):

    __version__ = "@"

    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self.data = {}

    def find(self, _id: int):
        return self.data.get(str(_id))

    def find_all(self):
        return self.data

    def insert(self, _id: int, _data: dict[str, Any]):
        self.data[str(_id)] = _data
        return True

def setup(config: dict):
    return MemoryDriver(config)
