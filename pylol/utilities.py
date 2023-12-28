import datetime

from enum import Enum

import arrow
import cassiopeia

from .config import RIOT_CONFIG
from .match import Match
from .player import Player


def _get_params(obj: dict, params: dict) -> dict:
    _r = {
        _s: _v for _s, _v in obj.items()
        if _s in params
    }

    for _s, _v in _r.items():
        if isinstance(_v, Enum):
            _r[_s] = _v.name
        elif isinstance(_v, (datetime.datetime, arrow.Arrow)):
            _r[_s] = _v.timestamp()
        elif isinstance(_v, datetime.timedelta):
            _r[_s] = _v.seconds
        elif isinstance(_v, dict):
            raise ValueError("Dictionaries are not supported.")
        elif isinstance(_v, list):
            raise ValueError("Lists are not supported.")

    return _r

def _dump_participant_to_dict(participant: Player) -> dict:
    stats = _get_params(participant.stats.to_dict(), RIOT_CONFIG["params"]["stats"])

    return {
        "player_id": participant.player_id,
        "champion": participant.championId,
        "team_position": participant.individualPosition,
        "stats": stats
    }

def _dump_match_to_dict(match: cassiopeia.Match) -> dict:
    return _get_params(match.to_dict(), RIOT_CONFIG["params"]["match"])

def get_match(match_id: int) -> cassiopeia.Match:
    return cassiopeia.get_match(match_id, region=cassiopeia.Region.europe_west)

def team_players_in_match(match: cassiopeia.Match, check_same_team: bool = True) -> \
        list[Player]:
    if isinstance(match, int):
        match = get_match(match)

    players = [
        _p for _p in match.participants
        if _p.summoner.id in RIOT_CONFIG.team.values()
    ]

    if check_same_team and not all(players[0].team == _p.team for _p in players):
        raise ValueError("Not all members are in the same team.")

    return [Player.from_dict(_p.to_dict()) for _p in players]

def dump_match_to_dict(match: cassiopeia.Match) -> dict:
    if isinstance(match, int):
        match = get_match(match)

    team_players = team_players_in_match(match)

    players = [
        {
            "match_id": match.id,
            **_dump_participant_to_dict(_p)
        }
        for _p in team_players
    ]
    
    return {
        **_dump_match_to_dict(match),
        "players": players
        }
