import discord
import cassiopeia
import datapipelines

from discord.ext import commands

from pylol.about import __version__ as PYLOL_VERSION
from pylol.config import CONFIG as CORE_CONFIG
from pylol.utilities import dump_match_to_dict
from pylol.bot.utilities import save, exists


CONFIG = CORE_CONFIG["discord"]

TEAM = CONFIG["team"]
EMBED = CONFIG["embed"]

TEAM_MEMBERS = TEAM["users"].values()

def get_intents():
    if "intents" not in CONFIG:
        return discord.Intents.default()

    intents = discord.Intents.none()

    for intent in CONFIG["intents"]:
        setattr(intents, intent, True)

    return intents

def main():

    bot = commands.Bot("!", intents=get_intents())



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
            f"Estoy vivo! 🤖\n" \
            f"Versión: **pylol-{PYLOL_VERSION}**\n" \
            f"Latencia: {emoji} ({latency}ms)",
            ephemeral=True)



    @bot.hybrid_command(
        name="partida",
        description="Indica que una partida se ha jugado")
    async def partida(ctx: commands.Context, id: int):
        if ctx.author.id not in TEAM_MEMBERS:
            return

        if exists(id):
            await ctx.send("Esta partida ya está registrada", ephemeral=True)
            return

        await ctx.defer(ephemeral=True)

        _match = cassiopeia.get_match(id, region=cassiopeia.Region.europe_west)

        try:
            match_stats = dump_match_to_dict(_match)
        except datapipelines.common.NotFoundError:
            await ctx.send("Partida no encontrada", ephemeral=True)
            return
        except ValueError:
            await ctx.send("Esta partida no es válida", ephemeral=True)
            return

        save(match_stats)

        embed=discord.Embed(
            title="Registro completado! 🤮",
            description=f"Se ha registrado la partida **{id}** correctamente",
            color=EMBED["color"]
            )
        embed.set_footer(text=EMBED["footer"])

        await ctx.send(embed=embed)



    @bot.command()
    async def sync(ctx: commands.Context):
        if not await bot.is_owner(ctx.author):
            return

        await bot.tree.sync()

        await ctx.send("Comandos sincronizados! 🗿")



    bot.run(CONFIG["api_key"])
