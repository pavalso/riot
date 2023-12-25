from typing import Any

import pymongo


class Driver:

    __version__ = pymongo.__version__

    def __init__(self, config):
        self.config = config
        self.client = pymongo.MongoClient(config["uri"])
        self.doc = self.client[config["database"]][config["collection"]]

    def find(self, _id: Any):
        return self.doc.find_one({"_id": _id})

    def find_all(self):
        return { _d["_id"]: _d for _d in self.doc.find() }

    def insert(self, _id: Any, _data: dict):
        _data["_id"] = _id
        return self.doc.insert_one(_data)

    def update(self):
        pass

    def delete(self):
        pass

def setup(config: dict):
    return Driver(config)
