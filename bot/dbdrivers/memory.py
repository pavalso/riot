from typing import Any

from bot.driver import Driver
from pylol import Match


class MemoryDriver(Driver):

    __version__ = "@"

    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self.data = {}

    def find(self, _id: Any):
        return self.data.get(_id)

    def find_all(self):
        return self.data

    def insert(self, match: Match):
        self.data[match.id] = match
        return True

    def drop_all(self) -> bool:
        self.data = {}
        return True

def setup(config: dict):
    return MemoryDriver(config)
