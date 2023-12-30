import os
import time

from typing import Any

import pandas
import humanize
import discord

from bot.config import DISCORD_CONFIG
from bot.driver import DB_DRIVER
from bot.exceptions import InvalidMatchError, MatchAlreadyExistsError

from pylol import Match


humanize.activate("es")

START_TIME = time.perf_counter_ns()

def save_match(match: Match) -> Match:
    if match is None:
        raise InvalidMatchError("Invalid match object")

    if match_exists(match.matchId):
        raise MatchAlreadyExistsError(f"Match {match.matchId} already exists")

    DB_DRIVER.insert(match)

    return match

def get_match(match_id: Any) -> Match:
    return DB_DRIVER.find(match_id)

def get_all_matches() -> dict[Any, Match]:
    return DB_DRIVER.find_all()

def match_exists(match_id: Any):
    return get_match(match_id) is not None

def generate_embed(title, description, *args, footer: str = None, error: bool = False, **kwargs):
    if "color" in kwargs:
        color = kwargs.pop("color")
    else:
        color = DISCORD_CONFIG.embed.error_color if error else DISCORD_CONFIG.embed.primary_color
    return discord.Embed(
        title=title,
        description=description,
        color=color,
        *args,
        **kwargs
    ).set_footer(text=footer or DISCORD_CONFIG.embed.footer)

def get_uptime() -> pandas.Timedelta:
    return pandas.Timedelta(time.perf_counter_ns() - START_TIME)

def dev_complete_cleanup():
    if not os.getenv("DEVELOPMENT") or not DB_DRIVER:
        return
    DB_DRIVER.drop_all()
