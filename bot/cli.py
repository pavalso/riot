import os
import asyncio
import dotenv
import yaml

import discord

from discord.ext import commands

from bot.config import DISCORD_CONFIG, load_configuration as load_bot_configuration
from bot.logger import configurate_logger
from pylol import load_configuration as load_pylol_configuration


def _get_conf() -> dict:
    try:
        _conf_file = os.getenv("CONFIG_FILE_NAME") or "config.yaml"
        with open(
            _conf_file,
            'r', 
            encoding="UTF-8") as stream:
            return yaml.load(stream.read(), Loader=yaml.FullLoader)
    except FileNotFoundError as exc:
        raise ValueError(
            f"Configuration file {_conf_file} not found. " \
            "Please make sure it exists in the root directory."
            ) from exc

def _get_intents():
    intents = discord.Intents.none()

    for intent in DISCORD_CONFIG.intents:
        setattr(intents, intent, True)

    return intents

async def _load_extensions(_bot: commands.Bot):
    await _bot.load_extension("bot.commands.pylol")
    await _bot.load_extension("bot.commands.base")

    if os.getenv("DEVELOPMENT"):
        await _bot.load_extension("bot.commands.debug")

def main():
    dotenv.load_dotenv()
    load_bot_configuration(load_pylol_configuration(_get_conf()))
    configurate_logger()

    from bot.driver import load_driver

    load_driver()

    bot = commands.Bot(command_prefix=DISCORD_CONFIG["prefix"], intents=_get_intents())
    asyncio.run(_load_extensions(bot))
    bot.run(DISCORD_CONFIG["api_key"], log_handler=None)
