import os
from typing import Any

import cassiopeia


class Configuration(object):

    def __init__(self):
        self._config = {}

    def load(self, _config: dict):
        self._config = { } if _config is None else _config
        return self

    def get(self, name: str, default: Any = None):
        return self._config.get(name, default)

    def __getattr__(self, name):
        return self._config.get(name)

    def __getitem__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self._config[name]

    def to_dict(self):
        return self._config

class TeamConfiguration(Configuration):
    name: str
    members: list

class ApiConfiguration(Configuration):
    api_key: str
    team: dict[int, Any]

class RiotConfiguration(ApiConfiguration):
    pass


CONFIG = { }
TEAM_CONFIG = TeamConfiguration()
RIOT_CONFIG = RiotConfiguration()

def load_configuration(config: dict, api_key: str = None):
    CONFIG.update(config)
    TEAM_CONFIG.load(config.get("team", {}))
    RIOT_CONFIG.load(config.get("riot", {}))

    _k = api_key or os.getenv("RIOT_API_KEY") or RIOT_CONFIG.api_key

    if _k is None:
        raise ValueError(
            "No API key found. Please set the environment variable RIOT_API_KEY to your API key." \
            "Alternatively, you can set the api_key field of riot in config.yaml."
            )

    cassiopeia.set_riot_api_key(_k)
