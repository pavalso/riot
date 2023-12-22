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

TEAM = CONFIG["team"]
PARAMS = CONFIG["params"]

API_KEY = os.getenv("RIOT_API_KEY") or CONFIG.get("riot_api_key")

if API_KEY is None:
    raise ValueError(
        "No API key found. Please set the environment variable RIOT_API_KEY to your API key." \
        "Alternatively, you can set the riot_api_key field in config.yaml."
        )

cassiopeia.set_riot_api_key(API_KEY)

def team_players_in_match(match: cassiopeia.Match, check_same_team: bool = True) -> list[cassiopeia.core.match.Participant]:
    players = [
        _p for _p in match.participants
        if _p.summoner.id in TEAM["members"]
    ]

    if not players:
        raise ValueError("No team members found in match.")

    if check_same_team and not all(players[0].team == _p.team for _p in players):
        raise ValueError("Not all members are in the same team.")
    
    return players

def _dump_participant_to_dict(participant: cassiopeia.core.match.Participant) -> dict:
    stats: dict = { 
        _s: _v for _s, _v in participant.stats.to_dict().items()
        if _s in PARAMS["stats"]
    }

    return {
        "champion": participant.champion.id,
        "team_position": participant.team_position.value,
        "stats": stats
    }

def dump_match_to_dict(match: cassiopeia.Match) -> dict:
    team_players = team_players_in_match(match)

    match_stats = {
        _s: _v for _s, _v in match.to_json().items()
        if _s in PARAMS["match"]
    }

    players = {
        _p.summoner.id: _dump_participant_to_dict(_p)
        for _p in team_players
    }

    return {
        match.id: {
                "match": match_stats,
                "players": players
            }
        }

if __name__ == "__main__":
    import json

    cass_match = cassiopeia.get_match(6724741545, cassiopeia.Region.europe_west)

    match_info = dump_match_to_dict(cass_match)

    with open(
            "test.json",
            "w",
            encoding="UTF-8") as stream:
        stream.write(
            json.dumps(
                match_info,
                indent=4
                )
            )
