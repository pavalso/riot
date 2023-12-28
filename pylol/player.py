import inspect

from dataclasses import dataclass, asdict

from .stats import Stats


@dataclass
class Player:

    player_id: str
    championId: int = None
    individualPosition: str = None
    stats: Stats = None

    def __post_init__(self):
        self.stats = Stats.from_dict(self.stats) if isinstance(self.stats, dict) else self.stats

    @classmethod
    def from_dict(cls, data: dict):
        summoner_id = data["summonerId"]
        return Player(summoner_id, **{k: v for k, v in data.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict:
        return asdict(self)
