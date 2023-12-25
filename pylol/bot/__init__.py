import asyncio

import discord

from discord.ext import commands

from pylol.config import CONFIG as CORE_CONFIG


CONFIG = CORE_CONFIG["discord"]

def get_intents():
    if "intents" not in CONFIG:
        return discord.Intents.default()

    intents = discord.Intents.none()

    for intent in CONFIG["intents"]:
        setattr(intents, intent, True)

    return intents

bot = commands.Bot(CONFIG["prefix"], intents=get_intents())

async def load_extensions():
    await bot.load_extension("pylol.bot.commands.pylol")
    await bot.load_extension("pylol.bot.commands.base")

    if CORE_CONFIG.get("development"):
        await bot.load_extension("pylol.bot.commands.debug")

def main():
    asyncio.run(load_extensions())
    bot.run(CONFIG["api_key"])
