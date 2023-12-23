import os
import yaml

import dotenv
import cassiopeia


dotenv.load_dotenv()

try:
    CONFIG_FILE_NAME = os.getenv("CONFIG_FILE_NAME") or "config.yaml"
    with open(
            CONFIG_FILE_NAME,
            'r', 
            encoding="UTF-8") as stream:
        CONFIG: dict = yaml.load(stream.read(), Loader=yaml.FullLoader)
except FileNotFoundError as exc:
    raise ValueError(
        f"Configuration file {CONFIG_FILE_NAME} not found. " \
        "Please make sure it exists in the root directory."
        ) from exc

RIOT_CONFIG = CONFIG["riot"]
TEAM_CONFIG = CONFIG["team"]

def init_key():
    _k = os.getenv("RIOT_API_KEY") or RIOT_CONFIG.get("api_key")

    os.environ.pop("RIOT_API_KEY", None)

    RIOT_CONFIG.pop("api_key", None)

    if _k is None:
        raise ValueError(
            "No API key found. Please set the environment variable RIOT_API_KEY to your API key." \
            "Alternatively, you can set the api_key field of riot in config.yaml."
            )

    cassiopeia.set_riot_api_key(_k)
