from discord.ext import commands

from bot.config import DISCORD_CONFIG
from bot import bot


TEAM_MEMBERS = DISCORD_CONFIG["team"].values()

DEFAULT_ERROR_MESSAGE = "No puedes ejecutar este comando."

async def is_owner(ctx):
    if not await bot.is_owner(ctx.author):
        raise commands.NotOwner(DEFAULT_ERROR_MESSAGE)
    return True

def is_team_member(ctx):
    if not ctx.author.id in TEAM_MEMBERS:
        raise commands.CheckFailure(DEFAULT_ERROR_MESSAGE)
    return True
