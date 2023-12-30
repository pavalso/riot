import json

from unittest.mock import patch

import datapipelines

from mocks import MockSummoner, MockPlayer, MockMatch, LoadConfigTest

import pylol


class TestPylolUtilities(LoadConfigTest):

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

    @patch("cassiopeia.get_match")
    def test_match_from_id(self, mock_get_match):
        mock_get_match.return_value = self.MATCH_1

        _m1: pylol.Match = pylol.Match.from_id(1)

        self.assertIsNotNone(_m1)
        self.assertIsInstance(_m1, pylol.Match)
        self.assertIsNotNone(_m1.matchId)
        self.assertEqual(_m1.matchId, 1)
        self.assertIsNotNone(_m1.participants)
        self.assertEqual(len(_m1.participants), 10)

        _p0: pylol.Player = _m1.participants[0]

        self.assertIsInstance(_p0, pylol.Player)
        self.assertIsNotNone(_p0.summonerId)
        self.assertIsNotNone(_p0.stats)

        _s0: pylol.Stats = _p0.stats

        self.assertIsInstance(_s0, pylol.Stats)
        self.assertIsNotNone(_s0.physicalDamageDealt)

        mock_get_match.side_effect = datapipelines.common.NotFoundError

        _m_not_exists: pylol.Match = pylol.Match.from_id(0)

        self.assertIsNone(_m_not_exists)

    #TODO: Fix this test
    @patch("cassiopeia.get_match")
    def test_team_players_in_match(self, mock_get_match):
        mock_get_match.return_value = self.MATCH_1

        _m1 = pylol.Match.from_id(1)
        _must_have_5 = _m1.team_players

        self.assertEqual(len(_must_have_5), 5)

        mock_get_match.return_value = self.MATCH_2

        _m2 = pylol.Match.from_id(2)
        _must_have_3 = _m2.team_players

        self.assertEqual(len(_must_have_3), 3)

        _p0 = _must_have_3[0]

        self.assertIsInstance(_p0, pylol.Player)
        self.assertIsNotNone(_p0.summonerId)
        self.assertIsNotNone(_p0.stats)

        _s0 = _p0.stats

        self.assertIsInstance(_s0, pylol.Stats)
        self.assertIsNotNone(_s0.physicalDamageDealt)

    #TODO: Fix this test
    @patch("cassiopeia.get_match")
    def test_match_to_dict(self, mock_get_match):
        mock_get_match.return_value = self.MATCH_1

        _m1 = pylol.Match.from_id(1)
        _d1 = _m1.to_dict()

        self.assertIsInstance(_d1, dict)

        _match_attributes = ["matchId", "mode", "duration", "participants", "team_players"]

        self.assertTrue(
            all(_attr in _d1 for _attr in _match_attributes)
            )

        self.assertTrue(
            all(_d1[_attr] is not None for _attr in _match_attributes)
        )

        self.assertEqual(len(_d1["team_players"]), 5)
        self.assertTrue(
            all(
                _attr["summonerId"] in pylol.RIOT_CONFIG.team.values()
                for _attr in _d1["team_players"])
        )

        mock_get_match.return_value = self.MATCH_2

        _m1 = pylol.Match.from_id(2)

        self.assertIsNotNone(_m1)

        self.assertEqual(len(_m1.team_players), 3)

    @patch("cassiopeia.get_match")
    def test_match_to_dict_can_be_json_serialized(self, mock_get_match):
        mock_get_match.return_value = self.MATCH_1

        _m1 = pylol.Match.from_id(1)
        _d1 = _m1.to_dict()

        _json = json.dumps(_d1)

        self.assertIsInstance(_json, str)

    @patch("cassiopeia.get_match")
    def test_match_dict_reverts_to_match(self, mock_get_match):
        mock_get_match.return_value = self.MATCH_1

        _m1 = pylol.Match.from_id(1)
        _d1 = _m1.to_dict()

        _m2 = pylol.Match.from_dict(_d1)
        _d2 = _m2.to_dict()

        self.assertEqual(_d1, _d2)

    def test_instantiate_match(self):
        _m1 = pylol.Match(
            1,
            matchId=1,
            queue=1,
            mode="CLASSIC",
            type="MATCHED_GAME",
            participants=[
                pylol.Player(
                    summonerId=1,
                    championId=1,
                    stats=pylol.Stats(
                        physicalDamageDealt=1
                        )
                    )
                ]
            )

        self.assertIsNotNone(_m1)
        self.assertIsNotNone(_m1.matchId)
        self.assertEqual(_m1.matchId, 1)
        self.assertIsNotNone(_m1.participants)
        self.assertEqual(len(_m1.participants), 1)

        _p0 = _m1.participants[0]

        self.assertIsInstance(_p0, pylol.Player)
        self.assertIsNotNone(_p0.summonerId)
        self.assertIsNotNone(_p0.stats)

        _s0 = _p0.stats

        self.assertIsInstance(_s0, pylol.Stats)
        self.assertIsNotNone(_s0.physicalDamageDealt)
