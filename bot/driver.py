import importlib

from abc import abstractmethod

from typing import Any

from bot.logger import LOGGER
from bot.config import DATABASE_CONFIG


class Driver:

    __version__: str = "?"

    def __init__(self, config) -> None:
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

class _DriverManager:

    def __init__(self, driver: Driver) -> None:
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


def _get_driver(driver: str) -> Driver:
    try:
        _module = importlib.import_module(f"{__package__}.dbdrivers.{driver}")
    except ImportError:
        _module = importlib.import_module(driver)
    LOGGER.info("Se ha cargado el driver %s", driver)
    return _module

def load_driver(driver: str) -> Driver:
    config = DATABASE_CONFIG["drivers"].get(driver) or {}
    LOGGER.debug("%s: %s", driver, config)
    return _get_driver(driver).setup(config)

DB_DRIVER = _DriverManager(load_driver(DATABASE_CONFIG["driver"]))
