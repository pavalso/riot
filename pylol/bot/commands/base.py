from discord.ext import commands

from pylol.bot.utilities import generate_embed


async def setup(bot: commands.Bot):

    @bot.tree.error
    async def on_error(_: commands.Context, __: Exception):
        return # On command not found error, do nothing



    @bot.event
    async def on_command_error(ctx: commands.Context, _: commands.CommandError):
        await ctx.send(
            embed=generate_embed(
                title="No puedes usar este comando! 🐀",
                description="Simplemente no puedes"
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
                description=
                    f"Estoy vivo! 🤖\n" \
                    f"Latencia: {emoji} ({latency}ms)"
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
