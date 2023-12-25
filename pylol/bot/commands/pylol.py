import datapipelines
import cassiopeia

from discord.ext import commands

from pylol.utilities import dump_match_to_dict
from pylol.bot.checks import is_team_member
from pylol.bot.utilities import save, exists, get_all, generate_embed


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
                            f"{i}. [{_id}](https://www.leagueofgraphs.com/es/match/euw/{_id})" 
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
            await send_ephemeral(ctx, "Esta partida ya está registrada")
            return

        await ctx.defer(ephemeral=True)

        _match = cassiopeia.get_match(_id, region=cassiopeia.Region.europe_west)

        try:
            match_stats = dump_match_to_dict(_match)
        except datapipelines.common.NotFoundError:
            await send_ephemeral(ctx, "Partida no encontrada")
            return
        except ValueError:
            await send_ephemeral(ctx, "Esta partida no es válida")
            return

        save(_id, match_stats)

        await send_ephemeral(ctx, "Partida encontrada", delete_after=5)

        await ctx.channel.send(
            embed=generate_embed(
                title="Registro completado! 🤮",
                description=f"Se ha registrado la partida **{_id}** correctamente"
                )
            )
