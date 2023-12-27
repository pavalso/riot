from discord.ext import commands

from bot.utilities import generate_embed
from bot.logger import LOGGER
from pylol.about import __version__ as PYLOL_VERSION


async def setup(bot: commands.Bot):

    @bot.before_invoke
    async def before_invoke(ctx: commands.Context):
        LOGGER.info(
            "%s ha ejecutado el comando %s",
            ctx.author, ctx.command.name)
        LOGGER.debug(
            "Contexto: %s, argumentos: %s %s",
            ctx, ctx.args, ctx.kwargs)



    @bot.tree.error
    async def on_error(_: commands.Context, error: Exception):
        LOGGER.exception("Se ha llamado on_error: %s", error)



    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError):

        async def send_ephemeral(*args, delete_after: int = None, **kwargs):
            await ctx.send(*args, ephemeral=True, delete_after=delete_after or 20, **kwargs)

        if isinstance(error, commands.CheckFailure):
            LOGGER.error("%s ha intentado ejecutar el comando %s sin permisos", ctx.author, ctx.command.name)
            await send_ephemeral(
                embed=generate_embed(
                    title="No puedes usar este comando! 🐀",
                    description="Simplemente no puedes",
                    error=True
                    )
                )
            return
        
        if isinstance(error, NotImplementedError):
            LOGGER.exception("El comando %s no está implementado", ctx.command.name)
            await send_ephemeral(
                embed=generate_embed(
                    title="Comando no implementado! 🐶",
                    description="Todavía no está implementado, espera a que lo haga",
                    error=True
                    )
                )
            return

        LOGGER.exception(
            "Se ha producido un error al ejecutar el comando %s",
            ctx.command.name)

        await send_ephemeral(
            embed=generate_embed(
                title="El comando ha fallado! 💀",
                description="Te has cargado el bot, felicidades",
                error=True
                )
            )



    @bot.hybrid_command(
        name="estado",
        description="Muestra el estado del bot")
    async def estado(ctx: commands.Context):
        latency = round(bot.latency * 1000)

        emoji = "🟢"

        if latency > 500:
            emoji = "🔴"
        elif latency > 350:
            emoji = "🟠"
        elif latency > 200:
            emoji = "🟡"

        await ctx.reply(
            embed=generate_embed(
                title="Estado del bot",
                description= \
                    "Estoy vivo! 🤖\n" \
                    f"Version: **{PYLOL_VERSION}**",
                footer=f"{emoji} ({latency}ms)"
                ),
            ephemeral=True)

    @bot.command(
        name="sync",
        description="Sincroniza los comandos con Discord"
    )
    @commands.is_owner()
    async def sync(ctx: commands.Context):
        await bot.tree.sync()
        await ctx.send("Comandos sincronizados! 🗿")
