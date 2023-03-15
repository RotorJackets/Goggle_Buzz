import discord
import random

from discord import app_commands
from discord.ext import commands
from lib.config import config


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="fight_song",
        description="Sends a random fight song quote",
    )
    async def fight_song(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            random.choice(config["fight_song_quotes"]), ephemeral=False
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
