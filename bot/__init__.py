import asyncio

import discord

from discord.ext import commands

from bot.config import DISCORD_CONFIG, CONFIG


def get_intents():
    if "intents" not in DISCORD_CONFIG:
        return discord.Intents.default()

    intents = discord.Intents.none()

    for intent in DISCORD_CONFIG["intents"]:
        setattr(intents, intent, True)

    return intents

bot = commands.Bot(DISCORD_CONFIG["prefix"], intents=get_intents())

async def load_extensions():
    await bot.load_extension("bot.commands.pylol")
    await bot.load_extension("bot.commands.base")

    if CONFIG.get("development"):
        await bot.load_extension("bot.commands.debug")

def main():
    asyncio.run(load_extensions())
    bot.run(DISCORD_CONFIG["api_key"])
