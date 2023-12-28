from typing import Any

import pymongo

from bot.driver import Driver


class MongoDBDriver(Driver):

    __version__ = pymongo.__version__

    def __init__(self, config):
        super().__init__(config)
        self.client = pymongo.MongoClient(self._config["uri"])
        self.doc = self.client[self._config["database"]][self._config["collection"]]

    def find(self, _id: Any):
        return self.doc.find_one({"_id": _id})

    def find_all(self):
        return { _d["_id"]: _d for _d in self.doc.find() }

    def insert(self, _id: Any, _data: dict):
        _data["_id"] = _id
        self.doc.insert_one(_data)
        return True

def setup(config):
    return MongoDBDriver(config)
