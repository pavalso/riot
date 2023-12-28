import dotenv
import os
import yaml

from bot import main as start_bot

from . import load_configuration



dotenv.load_dotenv()

try:
    _conf_file = os.getenv("CONFIG_FILE_NAME") or "config.yaml"
    with open(
            _conf_file,
            'r', 
            encoding="UTF-8") as stream:
        load_configuration(yaml.load(stream.read(), Loader=yaml.FullLoader))
except FileNotFoundError as exc:
    raise ValueError(
        f"Configuration file {_conf_file} not found. " \
        "Please make sure it exists in the root directory."
        ) from exc

start_bot()
