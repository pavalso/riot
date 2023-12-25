from discord.ext import commands

from pylol.config import CONFIG as CORE_CONFIG
from pylol.bot import bot


CONFIG = CORE_CONFIG["discord"]

TEAM_MEMBERS = CONFIG["team"]["users"].values()

DEFAULT_ERROR_MESSAGE = "No puedes ejecutar este comando."

async def is_owner(ctx):
    if not await bot.is_owner(ctx.author):
        raise commands.NotOwner(DEFAULT_ERROR_MESSAGE)
    return True

def is_team_member(ctx):
    if not ctx.author.id in TEAM_MEMBERS:
        raise commands.CheckFailure(DEFAULT_ERROR_MESSAGE)
    return True
