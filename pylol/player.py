import inspect

from dataclasses import dataclass, asdict

from .stats import Stats


@dataclass
class Player:

    id: str = None
    champion: int = None
    team_position: str = None
    stats: Stats = None

    def __post_init__(self):
        self.champion = int(self.champion) if self.champion else None
        self.stats = Stats.from_dict(self.stats) if self.stats else None

    @classmethod
    def from_dict(cls, data: dict):
        return Player(**{k: v for k, v in data.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict:
        return asdict(self)
