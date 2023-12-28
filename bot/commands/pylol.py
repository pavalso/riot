import datapipelines
import cassiopeia

from discord.ext import commands

from pylol.utilities import dump_match_to_dict
from bot.checks import is_team_member
from bot.utilities import save, exists, get_all, generate_embed
from bot.config import DISCORD_CONFIG
from bot.logger import LOGGER


async def send_ephemeral(ctx: commands.Context, *args, delete_after: int = None, **kwargs):
    await ctx.send(*args, ephemeral=True, delete_after=delete_after or 20, **kwargs)

async def setup(bot: commands.Bot):

    @bot.hybrid_command(
        name="listar",
        description="Lista las partidas registradas")
    @commands.check(is_team_member)
    async def listar(ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        await ctx.send(
            embed=generate_embed(
                title="Partidas registradas",
                description="\n".join(
                        [
                            f"{i}. [{_id}]({DISCORD_CONFIG.redirect_url})".format(id=_id) 
                            for i, _id in enumerate(get_all(), start=1)
                        ] 
                    ) or "No hay partidas registradas"
                )
            )

    @bot.hybrid_command(
        name="registrar",
        description="Indica que una partida se ha jugado")
    @commands.check(is_team_member)
    async def registrar(ctx: commands.Context, _id: int):
        if exists(_id):
            LOGGER.error("la partida %s ya está registrada", _id)
            await send_ephemeral(ctx, "Esta partida ya está registrada")
            return

        await ctx.defer(ephemeral=True)

        _match = cassiopeia.get_match(_id, region=cassiopeia.Region.europe_west)

        try:
            match_stats = dump_match_to_dict(_match)
        except datapipelines.common.NotFoundError:
            LOGGER.error("la partida %s no existe", _id)
            await send_ephemeral(ctx, "Partida no encontrada")
            return
        except ValueError as e:
            LOGGER.error("la partida %s no es válida %s, razón:", _id, e)
            await send_ephemeral(ctx, "Esta partida no es válida")
            return

        if len(match_stats["players"]) != 5:
            LOGGER.error("la partida %s no tiene 5 jugadores", _id)
            await send_ephemeral(ctx, "El equipo no está completo")
            return

        if _match.queue != cassiopeia.Queue.ranked_flex_fives \
                and _match.queue != cassiopeia.Queue.normal_draft_fives:
            LOGGER.error("la partida %s no es válida %s", _id, _match.queue.name)
            await send_ephemeral(ctx, "No es un tipo de partida válido")
            return

        save(_id, match_stats)

        LOGGER.info("%s ha registrado la partida %s", ctx.author, _id)

        await send_ephemeral(ctx, "Partida encontrada", delete_after=5)

        await ctx.send(
            embed=generate_embed(
                title="Registro completado! 🤮",
                description=f"Se ha registrado la partida **{_id}** correctamente"
                )
            )
