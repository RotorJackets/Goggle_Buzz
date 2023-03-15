import discord
from discord import app_commands
from discord.ext import commands


class test(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command(
        name="test",
        description="Test",
    )
    async def test(self, interaction: discord.Interaction, name: str) -> None:
        await interaction.response.send_message(
            f"Hello {name}",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(test(bot))
