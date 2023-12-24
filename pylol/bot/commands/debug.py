import sys
import discord

from discord.ext import commands

from pylol.bot.checks import is_owner
from pylol.bot.utilities import generate_embed
from pylol.bot.exceptions import Break
from pylol.about import __version__ as PYLOL_VERSION


async def setup(bot: commands.Bot):

    bot.add_check(is_owner)

    @bot.event
    async def on_ready():
        print("El bot está listo! 🤖")



    @bot.before_invoke
    async def before_invoke(ctx: commands.Context):
        if getattr(ctx, "__reinvoked__", False):
            return

        await reload()
        setattr(ctx, "__reinvoked__", True)

        if ctx in ctx.args:
            ctx.args.remove(ctx)

        await bot.get_command(ctx.command.name).callback(ctx, *ctx.args, **ctx.kwargs)

        raise Break



    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, Break):
            return

        await ctx.send(
            embed=generate_embed(
                title="Se ha producido un error! 💀",
                description=f"```{error}```",
                error=True
                ),
            ephemeral=True)



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

        description = \
            f"Estoy vivo! 🤖\n" \
            f"Versión: **{PYLOL_VERSION}**\n" \
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
            f"```" \
            #f"" \
            #f"```" \
            #f"Uptime: {bot.uptime}\n" \
            #f"```"

        await ctx.reply(
            embed=generate_embed(
                title="Estado del bot (DEV)",
                description=description
                ),
            ephemeral=True)

    bot.get_command("estado")._callback = estado



    @bot.hybrid_command(
        name="sync",
        description="Sincroniza los comandos con Discord"
    )
    async def sync(ctx: commands.Context):
        await bot.tree.sync()
        await ctx.send("Comandos sincronizados! 🗿")



    async def reload():
        extensions = bot.extensions.copy()
        for extension in extensions:
            await bot.reload_extension(extension)
        return bot.extensions
