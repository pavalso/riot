import os
import yaml

import dotenv
import cassiopeia


dotenv.load_dotenv()

try:
    with open(
            os.getenv("CONFIG_FILE_NAME") or "config.yaml",
            'r',
            encoding="UTF-8") as stream:
        CONFIG: dict = yaml.load(stream.read(), Loader=yaml.FullLoader)
except FileNotFoundError as exc:
    raise ValueError(
        "No config file found. Please create a config.yaml file in the root directory."
        ) from exc

TEAM = CONFIG["team"]

API_KEY = os.getenv("RIOT_API_KEY") or CONFIG.get("riot_api_key")

if API_KEY is None:
    raise ValueError(
        "No API key found. Please set the environment variable RIOT_API_KEY to your API key." \
        "Alternatively, you can set the riot_api_key field in config.yaml."
        )

cassiopeia.set_riot_api_key(API_KEY)

def team_players_in_match(match: cassiopeia.Match):
    return [
        _p for _p in match.participants
        if _p.summoner.puuid in TEAM["members"]
        ]

if __name__ == "__main__":
    print(team_players_in_match(cassiopeia.get_match(6724741545, cassiopeia.Region.europe_west)))
