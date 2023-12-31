import cassiopeia

from discord.ext import commands

from bot.checks import is_team_member
from bot.utilities import generate_embed, save_match, match_exists, get_all_matches
from bot.config import DISCORD_CONFIG
from bot.logger import LOGGER
from pylol import Match


async def send_ephemeral(ctx: commands.Context, *args, delete_after: int = None, **kwargs):
    await ctx.send(*args, ephemeral=True, delete_after=delete_after or 20, **kwargs)

async def setup(bot: commands.Bot):

    @bot.hybrid_command(
        name="listar",
        description="Lista las partidas registradas")
    @commands.check(is_team_member)
    async def listar(ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        _matches = get_all_matches()

        buff = "\n".join(
            [
                f"{i}. [{_id}]({DISCORD_CONFIG.redirect_url})".format(id=_id) 
                for i, _id in enumerate(_matches, start=1)
            ]
        ) or "No hay partidas registradas"

        await ctx.send(
            embed=generate_embed(
                title="Partidas registradas",
                description=buff
                )
            )



    @bot.hybrid_command(
        name="registrar",
        description="Indica que una partida se ha jugado")
    @commands.check(is_team_member)
    async def registrar(ctx: commands.Context, _id: int):
        if match_exists(_id):
            LOGGER.error("la partida %s ya está registrada", _id)
            await send_ephemeral(ctx, "Esta partida ya está registrada")
            return

        await ctx.defer(ephemeral=True)

        _match = Match.from_id(_id)

        if _match is None:
            LOGGER.error("la partida %s no existe", _id)
            await send_ephemeral(ctx, "Partida no encontrada")
            return

        if _match.queue != cassiopeia.Queue.ranked_flex_fives.id:
            LOGGER.error("la partida %s no es ranked: %s", _id, cassiopeia.Queue.from_id(_match.queue))
            await send_ephemeral(ctx, "Esta partida no es ranked 🤨")
            return

        if len(_match.team_players) != 5:
            LOGGER.error("la partida %s no tiene 5 jugadores", _id)
            await send_ephemeral(ctx, "El equipo no está completo 🤨")
            return

        save_match(_match)

        LOGGER.info("%s ha registrado la partida %s", ctx.author, _id)

        await send_ephemeral(ctx, "Partida encontrada", delete_after=5)

        await ctx.send(
            embed=generate_embed(
                title="Registro completado! 🤮",
                description=f"Se ha registrado la partida **{_id}** correctamente"
                )
            )
