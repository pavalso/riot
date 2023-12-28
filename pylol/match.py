import inspect

from dataclasses import dataclass, asdict

from .player import Player


@dataclass()
class Match:

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
    players: list[Player] = None

    def __post_init__(self):
        self.players = [Player.from_dict(player) for player in self.players] if isinstance(self.players, dict) else self.players

    @classmethod
    def from_dict(cls, data: dict):
        return Match(**{k: v for k, v in data.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict:
        return asdict(self)
