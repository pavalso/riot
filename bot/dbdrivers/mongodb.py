import pymongo

from bot.driver import Driver
from pylol import Match


class MongoDBDriver(Driver):

    __version__ = pymongo.__version__

    def __init__(self, config):
        super().__init__(config)
        self.client = pymongo.MongoClient(self._config["uri"])
        self.doc = self.client[self._config["database"]][self._config["collection"]]

    def find(self, _id: str):
        _m = self.doc.find_one({"_id": _id})
        return None if not _m else Match.from_dict(_m)

    def find_all(self):
        return {
                _m["_id"]: Match.from_dict(_m) \
                for _m in self.doc.find()
            }

    def insert(self, match: Match):
        _data = {
            "_id": match.id,
            **match.to_dict()
        }
        self.doc.insert_one(_data)
        return True

    def drop_all(self) -> bool:
        return self.doc.delete_many({})

def setup(config):
    return MongoDBDriver(config)
