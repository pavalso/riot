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
        self.matchId = int(self.matchId) if self.matchId else None
        self.gameStartTimestamp = int(self.gameStartTimestamp) if self.gameStartTimestamp else None
        self.gameEndTimestamp = int(self.gameEndTimestamp) if self.gameEndTimestamp else None
        self.gameDuration = int(self.gameDuration) if self.gameDuration else None
        self.creation = int(self.creation) if self.creation else None
        self.gameCreation = int(self.gameCreation) if self.gameCreation else None
        self.duration = int(self.duration) if self.duration else None
        self.start = float(self.start) if self.start else None
        self.mapId = int(self.mapId) if self.mapId else None
        self.private_game = bool(self.private_game) if self.private_game else None
        self.queue = int(self.queue) if self.queue else None
        self.players = [Player.from_dict(player) for player in self.players] if self.players else None

    @classmethod
    def from_dict(cls, data: dict):
        return Match(**{k: v for k, v in data.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict:
        return asdict(self)
