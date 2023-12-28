import os
import asyncio

import discord
import dotenv

from discord.ext import commands

from bot.config import DISCORD_CONFIG, load_configuration
from pylol.config import CONFIG


def get_intents():
    intents = discord.Intents.none()

    for intent in DISCORD_CONFIG.intents:
        setattr(intents, intent, True)

    return intents

async def load_extensions(bot: commands.Bot):
    await bot.load_extension("bot.commands.pylol")
    await bot.load_extension("bot.commands.base")

    if os.getenv("DEVELOPMENT"):
        await bot.load_extension("bot.commands.debug")

def main():
    dotenv.load_dotenv()
    load_configuration(CONFIG)
    bot = commands.Bot(command_prefix=DISCORD_CONFIG["prefix"], intents=get_intents())
    asyncio.run(load_extensions(bot))
    bot.run(DISCORD_CONFIG["api_key"], log_handler=None)
