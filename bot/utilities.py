import time

from typing import Any

import pandas
import humanize
import discord

from bot.config import DISCORD_CONFIG
from bot.driver import DB_DRIVER


humanize.activate("es")

EMBED = DISCORD_CONFIG["embed"]
START_TIME = time.perf_counter_ns()


def save(_id: Any, obj: dict):
    DB_DRIVER.insert(_id, obj)

def get(_id: Any):
    return DB_DRIVER.find(_id)

def get_all():
    return DB_DRIVER.find_all()

def exists(match_id: Any):
    return get(match_id) is not None

def generate_embed(title, description,*args, footer: str = None, error: bool = False, **kwargs):
    return discord.Embed(
        title=title,
        description=description,
        color= error and EMBED["error_color"] or EMBED["primary_color"],
        *args,
        **kwargs
    ).set_footer(text=footer or EMBED["footer"])

def get_uptime() -> pandas.Timedelta:
    return pandas.Timedelta(time.perf_counter_ns() - START_TIME)
