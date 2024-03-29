import logging.config
import yaml
import os

from bot.config import LOGGING_CONFIG


if conf_file := LOGGING_CONFIG.get("configuration_file"):
    if not os.path.isfile(conf_file):
        raise ValueError(
            f"Configuration file {conf_file} not found. " \
            "Please make sure it exists in the root directory."
            )

    with open(conf_file, "r", encoding="UTF-8") as f:
        logging.config.dictConfig(yaml.safe_load(f))
elif LOGGING_CONFIG:
    logging.config.dictConfig(LOGGING_CONFIG)

LOGGER = logging.getLogger("pylol")
