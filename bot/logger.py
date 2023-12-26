import logging.config
import yaml
import os


config = None

if os.path.isfile('logging.yaml'):
    with open('logging.yml', 'r') as f:
        config = yaml.safe_load(f)

if config:
    logging.config.dictConfig(config)

LOGGER = logging.getLogger("pylol")

LOGGER.setLevel(logging.DEBUG)
