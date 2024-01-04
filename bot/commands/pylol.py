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
                            f"{i}. [{_id}]({DISCORD_CONFIG['redirect_url']})".format(id=_id) 
                            for i, _id in enumerate(get_all(), start=1)
                        ] 
                    ) or "No hay partidas registradas"
                )
            )

    @bot.hybrid_command(
        name="registrar",
        description="Indica que una partida se ha jugado")
    @commands.check(is_team_member)
    async def registrar(ctx: commands.Context, id: int):
        if exists(id):
            LOGGER.error("la partida %s ya está registrada", id)
            await send_ephemeral(ctx, "Esta partida ya está registrada")
            return

        await ctx.defer(ephemeral=True)

        _match = cassiopeia.get_match(id, region=cassiopeia.Region.europe_west)

        try:
            match_stats = dump_match_to_dict(_match)
        except datapipelines.common.NotFoundError:
            LOGGER.error("la partida %s no existe", id)
            await send_ephemeral(ctx, "Partida no encontrada")
            return
        except ValueError as e:
            LOGGER.error("la partida %s no es válida %s, razón:", id, e)
            await send_ephemeral(ctx, "Esta partida no es válida")
            return

        if _match.queue != cassiopeia.Queue.ranked_flex_fives:
            LOGGER.error("la partida %s no es ranked: %s", id, _match.queue)
            await send_ephemeral(ctx, "Esta partida no es ranked 🤨")
            return
        
        if len(match_stats["players"]) != 5:
            LOGGER.error("la partida %s no tiene 5 jugadores", id)
            await send_ephemeral(ctx, "El equipo no está completo 🤨")
            return

        save(id, match_stats)

        LOGGER.info("%s ha registrado la partida %s", ctx.author, id)

        await send_ephemeral(ctx, "Partida encontrada", delete_after=5)

        await ctx.send(
            embed=generate_embed(
                title="Registro completado! 🤮",
                description=f"Se ha registrado la partida **{id}** correctamente"
                )
            )
