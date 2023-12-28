import unittest
import yaml
import cassiopeia

from typing import NamedTuple

import pylol


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
    stats: MockStats = MockStats()

    def to_dict(self):
        return {
            "summonerId": self.summoner.id,
            "championId": self.champion.id,
            "individualPosition": self.lane.value,
            "stats": self.stats.to_dict()
            }

class MockMatch(NamedTuple):

    participants: list[MockPlayer]
    id: int = 1
    mode: str = "TEST_MODE"
    duration: int = 250

    def to_dict(self):
        return {
            "matchId": self.id,
            "mode": self.mode,
            "duration": self.duration,
            "participants": [p.to_dict() for p in self.participants]
            }


class TestPylolUtilities(unittest.TestCase):

    TEAM_1 = [
        MockPlayer(
            MockSummoner("rid-1")
            ),
        MockPlayer(
            MockSummoner("rid-2")
            ),
        MockPlayer(
            MockSummoner("rid-3")
            ),
        MockPlayer(
            MockSummoner("rid-4")
            ),
        MockPlayer(
            MockSummoner("rid-5")
            )
        ]

    TEAM_2 = [
        MockPlayer(
            MockSummoner("rid-3")
            ),
        MockPlayer(
            MockSummoner("rid-4")
            ),
        MockPlayer(
            MockSummoner("rid-1")
            ),
        MockPlayer(
            MockSummoner("n-1")
            ),
        MockPlayer(
            MockSummoner("n-2")
            )
        ]

    NOT_TEAM = [
        MockPlayer(
            MockSummoner("n-6")
            ),
        MockPlayer(
            MockSummoner("n-7")
            ),
        MockPlayer(
            MockSummoner("n-8")
            ),
        MockPlayer(
            MockSummoner("n-9")
            ),
        MockPlayer(
            MockSummoner("n-10")
            )
        ]

    MATCH_1 = MockMatch(
        [
            *TEAM_1,
            *NOT_TEAM
            ]
        )

    MATCH_2 = MockMatch(
        [
            *TEAM_2,
            *NOT_TEAM
            ]
        )

    @classmethod
    def setUp(cls) -> None:
        with open("tests/test.config.yaml", "r", encoding="UTF-8") as f:
            pylol.load_configuration(yaml.safe_load(f), api_key="test-key")

    def test_team_players_in_match(self):
        must_have_5 = pylol.team_players_in_match(self.MATCH_1)

        self.assertEqual(len(must_have_5), 5)
        self.assertTrue(all([_p.player_id in pylol.RIOT_CONFIG.team.values() for _p in must_have_5]))

        must_have_3 = pylol.team_players_in_match(self.MATCH_2)

        self.assertEqual(len(must_have_3), 3)

    def test_dump_match_to_dict(self):
        _dump_match_1 = pylol.dump_match_to_dict(self.MATCH_1)

        self.assertIsInstance(_dump_match_1, dict)

        _match_attributes = ["matchId", "mode", "duration", "players"]

        self.assertTrue(all(_attr in _dump_match_1 for _attr in _match_attributes))

        _must_have_5_players = _dump_match_1["players"]

        self.assertEqual(len(_must_have_5_players), 5)

        _player_attributes = ["player_id", "match_id", "champion", "team_position", "stats"]

        self.assertTrue(all(_attr in _must_have_5_players[0] for _attr in _player_attributes))

        _stats_attributes = ["physicalDamageDealt", "visionScore", "goldSpent", "goldEarned", "totalHeal"]

        self.assertTrue(all(_attr in _must_have_5_players[0]["stats"] for _attr in _stats_attributes))
