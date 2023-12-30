import discord

from mocks import LoadConfigTest
from parameterized import parameterized

import bot

from bot.config import load_configuration, DISCORD_CONFIG
from bot.driver import load_driver

from pylol import Match, Player


class TestBotUtilities(LoadConfigTest):

    driver_config = None

    MATCH_1 = Match(
        1,
        matchId=1,
        queue=1,
        mode="CLASSIC",
        type="MATCHED_GAME",
        participants=[
            Player(summonerId=1,
                   championId=1,
                   stats={}
                   )
                ]
        )

    @classmethod
    def setUp(cls) -> None:
        cls.driver_config = load_configuration(super().setUp())["database"]

    @parameterized.expand([
        "memory", "local", "mongodb"
        ])
    def test_save_match(self, driver):
        _conf = self.driver_config.copy()
        _conf["driver"] = driver
        load_driver(_conf)

        _m1 = bot.save_match(self.MATCH_1)

        self.assertIsNotNone(_m1)
        self.assertEqual(_m1, self.MATCH_1)

        with self.assertRaises(bot.exceptions.InvalidMatchError):
            bot.save_match(None)

        with self.assertRaises(bot.exceptions.MatchAlreadyExistsError):
            bot.save_match(self.MATCH_1)

    @parameterized.expand([
        "memory", "local", "mongodb"
        ])
    def test_get_match(self, driver):
        _conf = self.driver_config.copy()
        _conf["driver"] = driver
        load_driver(_conf)

        _m1 = bot.get_match(1)

        self.assertIsNone(_m1)

        bot.save_match(self.MATCH_1)

        _m1 = bot.get_match(1)

        self.assertIsNotNone(_m1)
        self.assertEqual(_m1, self.MATCH_1)

    @parameterized.expand([
        "memory", "local", "mongodb"
        ])
    def test_match_exists(self, driver):
        _conf = self.driver_config.copy()
        _conf["driver"] = driver
        load_driver(_conf)

        self.assertFalse(bot.match_exists(1))

        bot.save_match(self.MATCH_1)

        self.assertTrue(bot.match_exists(1))

    @parameterized.expand([
        "memory", "local", "mongodb"
        ])
    def test_get_all_matches(self, driver):
        _conf = self.driver_config.copy()
        _conf["driver"] = driver
        load_driver(_conf)
        
        _m_empty = bot.get_all_matches()

        self.assertIsInstance(_m_empty, dict)
        self.assertFalse(_m_empty)

        bot.save_match(self.MATCH_1)

        _m_1 = bot.get_all_matches()

        self.assertIsInstance(_m_1, dict)
        self.assertTrue(_m_1)
        self.assertEqual(_m_1[1], self.MATCH_1)

    def test_generate_embed(self):
        _no_color_embed = bot.generate_embed(
            title="test",
            description="test"
        )

        self.assertIsInstance(_no_color_embed, discord.Embed)
        self.assertEqual(_no_color_embed.title, "test")
        self.assertEqual(_no_color_embed.description, "test")
        self.assertEqual(_no_color_embed.footer.text, DISCORD_CONFIG.embed.footer)
        self.assertEqual(_no_color_embed.color.value, DISCORD_CONFIG.embed.primary_color)

        _error_embed = bot.generate_embed(
            title="test",
            description="test",
            error=True
        )

        self.assertIsInstance(_error_embed, discord.Embed)
        self.assertEqual(_error_embed.color.value, DISCORD_CONFIG.embed.error_color)

        _color_embed = bot.generate_embed(
            title="test",
            description="test",
            color=0x000000
        )

        self.assertIsInstance(_color_embed, discord.Embed)
        self.assertEqual(_color_embed.color.value, 0x000000)

    def tearDown(self) -> None:
        bot.dev_complete_cleanup()
