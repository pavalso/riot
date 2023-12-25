import importlib

from typing import Any

from pylol.config import CONFIG


class _DbDriver():

    @staticmethod
    def setup(config: dict) -> Any:
        pass

    @staticmethod
    def find(_id: Any) -> Any:
        pass

    @staticmethod
    def find_all() -> Any:
        pass

    @staticmethod
    def insert(_id: Any, _data: dict[str, Any]) -> Any:
        pass

    @staticmethod
    def update(_id: Any, _new_data: dict[str, Any]) -> Any:
        pass

    @staticmethod
    def delete(_id: Any) -> Any:
        pass

def get_driver(driver: str) -> _DbDriver:
    try:
        return importlib.import_module(f"{__package__}.dbdrivers.{driver}")
    except ImportError:
        return importlib.import_module(driver)


DATABASE_CONFIG = CONFIG["database"]

_driver = get_driver(DATABASE_CONFIG["driver"])

DB_DRIVER = _driver.setup(DATABASE_CONFIG[DATABASE_CONFIG["driver"]]) or _driver
