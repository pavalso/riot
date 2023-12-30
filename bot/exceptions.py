from discord.ext import commands


class Break(commands.CommandError):
    pass

class InvalidMatchError(Exception):
    pass

class MatchAlreadyExistsError(Exception):
    pass
