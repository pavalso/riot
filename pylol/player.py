from dataclasses import dataclass

import cassiopeia

from .stats import Stats
from .common import PylolObject


@dataclass
class Player(PylolObject):

    summonerId: str
    championId: int = None
    teamPosition: cassiopeia.Lane = None
    visionClearedPings: int = None
    isBot: bool = None
    dangerPings: int = None
    pushPings: int = None
    getBackPings: int = None
    allInPings: int = None
    basicPings: int = None
    enemyMissingPings: int = None
    assistMePings: int = None
    holdPings: int = None
    needVisionPings: int = None
    onMyWayPings: int = None
    baitPings: int = None
    enemyVisionPings: int = None
    commandPings: int = None
    stats: Stats = None

    def __post_init__(self):
        self.stats = Stats.from_dict(self.stats) \
            if isinstance(self.stats, dict) else self.stats
