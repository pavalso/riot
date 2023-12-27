import sys
import discord

import humanize

from discord.ext import commands

from bot.checks import is_owner
from bot.utilities import generate_embed, get_uptime
from bot.exceptions import Break
from bot.driver import DB_DRIVER
from pylol.about import __version__ as PYLOL_VERSION
from bot.logger import LOGGER


async def setup(bot: commands.Bot):

    old_before_invoke = bot._before_invoke
    old_on_command_error = bot.on_command_error
    old_on_ready = bot.on_ready

    bot.add_check(is_owner)



    @bot.event
    async def on_ready():
        LOGGER.warning("\x1b[31;20m¡ATENCION! ¡ESTE BOT ESTA EN MODO DE DESARROLLO!\x1b[0m 🚨")
        await old_on_ready()



    @bot.before_invoke
    async def before_invoke(ctx: commands.Context):
        await reload()

        if old_before_invoke:
            await old_before_invoke(ctx)

        if ctx in ctx.args:
            ctx.args.remove(ctx)

        try:
            await bot.get_command(ctx.command.name).callback(ctx, *ctx.args, **ctx.kwargs)
        except Exception as e:
            await bot.on_command_error(ctx, e)

        raise Break



    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, Break):
            return

        await old_on_command_error(ctx, error)



    @bot.hybrid_command(
        name="ping",
        description="Muestra la latencia del bot"
    )
    async def ping(ctx: commands.Context):
        await ctx.send("pong! 🗿")



    async def estado(ctx: commands.Context):
        latency = round(bot.latency * 1000)

        emoji = "🟢"

        if latency > 500:
            emoji = "🔴"
        elif latency > 350:
            emoji = "🟠"
        elif latency > 200:
            emoji = "🟡"

        uptime = get_uptime().to_pytimedelta()

        description = \
            f"Estoy vivo! 🤖\n" \
            f"Latencia: {emoji} ({latency}ms)" \
            f"" \
            f"```" \
            f"Comandos: {len(bot.commands)}\n" \
            f"Extensiones: {len(bot.extensions)}\n" \
            f"```" \
            f"" \
            f"```" \
            f"Python: {sys.version}\n" \
            f"Discord.py: {discord.__version__}\n" \
            f"pylol: {PYLOL_VERSION}\n" \
            f"Base de datos: {DB_DRIVER.__version__}\n" \
            f"```" \
            f"" \
            f"```" \
            f"Tiempo activo: {humanize.naturaldelta(uptime)}\n" \
            f"```"

        await ctx.reply(
            embed=generate_embed(
                title="Estado del bot (DEV)",
                description=description
                ),
            ephemeral=True)

    bot.get_command("estado")._callback = estado



    async def reload():
        extensions = bot.extensions.copy()
        for extension in extensions:
            await bot.reload_extension(extension)
        return bot.extensions
