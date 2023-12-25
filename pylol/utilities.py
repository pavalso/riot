import datetime

from enum import Enum

from pylol.config import RIOT_CONFIG as CONFIG

import arrow
import cassiopeia


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

def _dump_participant_to_dict(participant: cassiopeia.core.match.Participant) -> dict:
    stats = _get_params(participant.stats.to_dict(), CONFIG["params"]["stats"])

    return {
        "champion": participant.champion.id,
        "team_position": participant.team_position.value,
        "stats": stats
    }

def _dump_match_to_dict(match: cassiopeia.Match) -> dict:
    return _get_params(match.to_dict(), CONFIG["params"]["match"])

def team_players_in_match(match: cassiopeia.Match, check_same_team: bool = True) -> list[cassiopeia.core.match.Participant]:
    players = [
        _p for _p in match.participants
        if _p.summoner.id in CONFIG["team"]["members"].values()
    ]

    if check_same_team and not all(players[0].team == _p.team for _p in players):
        raise ValueError("Not all members are in the same team.")

    if len(players) != 5:
        raise ValueError("Match does not have 5 members of the team.")

    return players

def dump_match_to_dict(match: cassiopeia.Match) -> dict:
    team_players = team_players_in_match(match)

    match_stats = _dump_match_to_dict(match)

    players = {
        _p.summoner.id: _dump_participant_to_dict(_p)
        for _p in team_players
    }

    return {
        "match": match_stats,
        "players": players
    }
