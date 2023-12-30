from typing import NamedTuple

import unittest
import yaml
import cassiopeia
import arrow

import pylol


class LoadConfigTest(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        with open("tests/test.config.yaml", "r", encoding="UTF-8") as f:
            return pylol.load_configuration(yaml.safe_load(f), api_key="test-api-key")

class MockStats(NamedTuple):

    physicalDamageDealt: int = 1
    visionScore: int = 2
    goldSpent: int = 3
    goldEarned: int = 4
    totalHeal: int = 5

    def to_dict(self):
        return {
            "physicalDamageDealt": self.physicalDamageDealt,
            "visionScore": self.visionScore,
            "goldSpent": self.goldSpent,
            "goldEarned": self.goldEarned,
            "totalHeal": self.totalHeal
            }

class MockSummoner(NamedTuple):

    id: str

class MockChampion(NamedTuple):

    id: int

class MockPlayer(NamedTuple):

    @property
    def team(self):
        return self.summoner.id in pylol.RIOT_CONFIG.team.values()

    summoner: MockSummoner
    champion: MockChampion = MockChampion(33)
    lane: cassiopeia.Lane = cassiopeia.Lane.top_lane
    participantId: int = 1
    stats: MockStats = MockStats()

    def to_dict(self):
        return {
            "summonerId": self.summoner.id,
            "championId": self.champion.id,
            "teamPosition": self.lane,
            "participantId": self.participantId,
            "stats": self.stats.to_dict()
            }

class MockMatch(NamedTuple):

    participants: list[MockPlayer]
    id: int = 1
    mode: str = "TEST_MODE"
    duration: int = 250
    start: arrow.Arrow = arrow.now()

    def load(self, *args, **kwargs):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "matchId": self.id,
            "mode": self.mode,
            "duration": self.duration,
            "start": self.start,
            "participants": [p.to_dict() for p in self.participants]
            }
