import discord
from discord import app_commands
from discord.ext import commands, tasks

import cogs.velocidrone.velocidrone_helper as velocidrone_helper


class Velocidrone(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="velocidrone_leaderboard",
        description="Shows the leaderboard",
    )
    async def show_leaderboard(
        self,
        interaction: discord.Interaction,
        official: bool,
        race_mode: int,
        trackID: int,
        version: int,
        track_name: str = None,
    ):
        json_data = await velocidrone_helper.get_leaderboard(
            f"https://www.velocidrone.com/leaderboard_as_json2/{official}/{race_mode}/{trackID}/{version}"
        )
        pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Velocidrone(bot))
