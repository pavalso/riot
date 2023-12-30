import os
import logging.config

import yaml

from bot.config import LOGGING_CONFIG


def load_logger(config: dict = LOGGING_CONFIG):
    dev_logger = config.get("development_logger", "dev")
    prod_logger = config.get("production_logger", "prod")

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

    return logging.getLogger(dev_logger if os.getenv("DEVELOPMENT") else prod_logger)

LOGGER = load_logger()
