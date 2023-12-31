import os
import logging.config

import yaml

from bot.config import LOGGING_CONFIG


def configurate_logger(config: dict = LOGGING_CONFIG):
    if conf_file := config.get("configuration_file"):
        if not os.path.isfile(conf_file):
            raise ValueError(
                f"Configuration file {conf_file} not found. " \
                "Please make sure it exists in the root directory."
                )

        with open(conf_file, "r", encoding="UTF-8") as f:
            logging.config.dictConfig(yaml.safe_load(f))
    elif config.get("version") is not None:
        logging.config.dictConfig(config.to_dict())

LOGGER = logging.getLogger("pylol")
