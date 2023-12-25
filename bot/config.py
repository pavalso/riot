import importlib

from pylol.config import CONFIG
from bot.driver import Driver


def _get_driver(driver: str) -> Driver:
    try:
        return importlib.import_module(f"{__package__}.dbdrivers.{driver}")
    except ImportError:
        return importlib.import_module(driver)

def load_driver(driver: str) -> Driver:
    return _get_driver(driver).setup(DATABASE_CONFIG[driver])

DISCORD_CONFIG = CONFIG["discord"]
DATABASE_CONFIG = CONFIG["database"]

DB_DRIVER = load_driver(DATABASE_CONFIG["driver"])
