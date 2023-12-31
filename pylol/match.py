from dataclasses import dataclass

import cassiopeia
import datapipelines

from . import player as _player
from .config import RIOT_CONFIG
from .common import PylolObject


@dataclass
class Match(PylolObject):

    id: int
    matchId: int = None
    gameStartTimestamp: int = None
    gameEndTimestamp: int = None
    gameDuration: int = None
    creation: int = None
    mode: str = None
    gameCreation: int = None
    duration: int = None
    continent: str = None
    start: float = None
    type: str = None
    tournamentCode: str = None
    mapId: int = None
    private_game: bool = None
    queue: int = None
    version: str = None
    name: str = None
    platform: str = None
    participants: list[_player.Player] = None

    @property
    def team_players(self):
        return [p for p in self.participants if p.summonerId in RIOT_CONFIG.team.values()]

    def __post_init__(self):
        self._raw = { }
        self.participants = [
            _player.Player.from_dict(player) if isinstance(player, dict) else player
            for player in self.participants
            ]

    @staticmethod
    def from_id(match_id: int):
        try:
            _cm = cassiopeia.get_match(match_id, region=cassiopeia.Region.europe_west)
            _cm.load()
        except datapipelines.common.NotFoundError:
            return None
        except ValueError:
            return None

        _dict = _cm.to_dict()
        _players = _cm.participants
        for _dict_player, _raw_player in zip(_dict["participants"], _players):
            _dict_player["stats"]["kda"] = _raw_player.stats.kda

        return Match.from_dict(_dict)

    def to_dict(self):
        return {
            "team_players": [p.to_dict() for p in self.team_players],
            **super().to_dict()
            }
