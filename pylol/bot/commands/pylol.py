import datapipelines
import cassiopeia

from discord.ext import commands

from pylol.utilities import dump_match_to_dict
from pylol.bot.checks import is_team_member
from pylol.bot.utilities import save, exists, generate_embed


async def setup(bot: commands.Bot):

    @bot.hybrid_command(
        name="partida",
        description="Indica que una partida se ha jugado")
    @commands.check(is_team_member)
    async def partida(ctx: commands.Context, id: int):
        if exists(id):
            await ctx.send("Esta partida ya está registrada", ephemeral=True)
            return

        await ctx.defer()

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

        await ctx.send(
            embed=generate_embed(
                title="Registro completado! 🤮",
                description=f"Se ha registrado la partida **{id}** correctamente"
                )
            )
