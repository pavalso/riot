from pylol.config import CONFIG as CORE_CONFIG
from pylol.bot import bot


CONFIG = CORE_CONFIG["discord"]

TEAM_MEMBERS = CONFIG["team"]["users"].values()

async def is_owner(ctx):
    return await bot.is_owner(ctx.author)

def is_team_member(ctx):
    return ctx.author.id in TEAM_MEMBERS
