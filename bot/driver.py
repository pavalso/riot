import importlib

from abc import abstractmethod

from typing import Any

from bot.logger import LOGGER
from bot.match import Match
from bot.config import DATABASE_CONFIG


class Driver:

    __version__: str = "?"

    def __init__(self, config: dict) -> None:
        self._config = config

    @abstractmethod
    def find(self, _id: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def insert(self, _id: Any, _data: dict[str, Any]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, _id: Any, _new_data: dict[str, Any]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id: Any) -> bool:
        raise NotImplementedError

class _CoreDriver(Driver):

    __drivers: list[Driver]

    def __init__(self, drivers: list[Driver]) -> None:
        super().__init__({})
        self.__drivers = drivers
        self.__version__ = ", ".join([
            f"{driver.__class__.__name__} {driver.__version__}" for driver in drivers
            ])

    def _to_match(self, data: dict[str, Any]) -> Match:
        _match_dict = data["match"]

        players = []

        for _k, _player in data["players"].items():
            _player["id"] = _k
            players.append(_player)

        _match_dict["players"] = players

        return Match.from_dict(_match_dict)

    @staticmethod
    def load_drivers(drivers: list[str]) -> Driver:
        drivers = \
            [driver.lower() for driver in drivers] \
            if isinstance(drivers, list) else \
            [drivers.lower()]
        if len(drivers) == 0:
            raise ValueError("No drivers specified")
        return _CoreDriver([_load_driver(driver) for driver in drivers])

    def find(self, _id: Any) -> Any:
        _results = [(driver, driver.find(_id)) for driver in self.__drivers]

        LOGGER.debug(
            "Find %s, valores devueltos: %s", 
            _id, ", ".join([f"{_d.__class__.__name__} {_r is not None}" for _d, _r in _results])
            )

        _missing = [_d for _d, _r in _results if _r is None]
        _found = [(_d, _r) for _d, _r in _results if _r is not None]

        if len(_found) == 0:
            return None

        return _found[0][1]

    def find_all(self) -> Any:
        _results = [(driver, driver.find_all()) for driver in self.__drivers]

        LOGGER.debug(
            "Find all, valores devueltos: %s", 
            ", ".join([f"{_d.__class__.__name__} {len(_r)}" for _d, _r in _results])
            )

        return _results[0][1]

    def insert(self, _id: Any, _data: dict[str, Any]) -> Any:
        _results = [(driver, driver.insert(_id, _data)) for driver in self.__drivers]

        LOGGER.debug(
            "Insert %s, valores devueltos: %s", 
            _id, ", ".join([f"{_d.__class__.__name__} {_r is not None}" for _d, _r in _results])
            )

        return _results[0]

def _get_driver(driver: str) -> Driver:
    try:
        _module = importlib.import_module(f"{__package__}.dbdrivers.{driver}")
    except ImportError:
        _module = importlib.import_module(driver)
    LOGGER.info("Se ha cargado el driver %s", driver)
    return _module

def _load_driver(driver: str) -> Driver:
    config = DATABASE_CONFIG.get(driver) or {}
    LOGGER.debug("%s: %s", driver, config)
    return _get_driver(driver).setup(config)

DB_DRIVER = _CoreDriver.load_drivers(DATABASE_CONFIG["driver"])
