import importlib

from abc import abstractmethod

from typing import Any

from bot.logger import LOGGER
from bot.config import DATABASE_CONFIG, Configuration, DatabaseConfiguration
from pylol import Match


class Driver:

    __version__: str = "?"

    def __init__(self, config: Configuration) -> None:
        self._config = config

    @abstractmethod
    def find(self, _id: Any) -> Match:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> {Any: Match}:
        raise NotImplementedError

    @abstractmethod
    def insert(self, _data: dict[str, Match]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, _new_data: dict[str, Match]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def drop_all(self) -> bool:
        raise NotImplementedError

class _DriverManager:

    __version__: str = ""

    _driver: Driver = None

    def set_driver(self, driver: Driver) -> None:
        self._driver = driver
        self.__version__ = f"{self._driver.__class__.__name__} {self._driver.__version__}"

    def log(self, func) -> Any:
        def wrapper(*args, **kwargs):
            LOGGER.debug(
                "Ejecutando %s en %s con %s y %s",
                func.__name__, self._driver.__class__.__name__, args, kwargs)
            return func(*args, **kwargs)
        return wrapper

    def __getattribute__(self, __name: str) -> Any:
        if __name == "__version__":
            return super().__getattribute__(__name)
        return self.log(getattr(self._driver, __name)) \
            if __name in Driver.__dict__ \
            else super().__getattribute__(__name)

    def __bool__(self) -> bool:
        return bool(self._driver)


def _get_driver(driver: str) -> Driver:
    try:
        _module = importlib.import_module(f"{__package__}.dbdrivers.{driver}")
    except ImportError:
        _module = importlib.import_module(driver)
    LOGGER.info("Se ha cargado el driver %s", driver)
    return _module

def load_driver(config: DatabaseConfiguration = DATABASE_CONFIG) -> Driver:
    _manager: _DriverManager = DB_DRIVER
    driver = config["driver"]
    _config = (config.get("drivers") or {}).get(driver) or {}
    LOGGER.debug("%s: %s", driver, _config)
    _manager.set_driver(_get_driver(driver).setup(_config))
    return _manager

DB_DRIVER: Driver = _DriverManager()
