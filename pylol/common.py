import inspect
import datetime

from enum import Enum
from abc import  ABC
from dataclasses import dataclass, asdict


import arrow


@dataclass
class PylolObject(ABC):

    @staticmethod
    def _dict_factory(x):
        _r = { }
        for _s, _v in x:
            if isinstance(_v, Enum):
                _r[_s] = _v.value
            elif isinstance(_v, (datetime.datetime, arrow.Arrow)):
                _r[_s] = _v.timestamp()
            elif isinstance(_v, datetime.timedelta):
                _r[_s] = _v.seconds
            else:
                _r[_s] = _v
        return _r

    @classmethod
    def from_dict(cls, _dict: dict):
        return cls(**{k: v for k, v in _dict.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=self._dict_factory)
