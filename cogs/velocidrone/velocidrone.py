import discord
from discord import app_commands
from discord.ext import commands, tasks

import cogs.velocidrone.velocidrone_helper as velocidrone_helper
from lib.config import config as config_main

config = config_main["velocidrone"]


class Velocidrone(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        velocidrone_helper.setup()

    @app_commands.command(
        name="velocidrone_leaderboard",
        description="Shows the leaderboard",
    )
    async def velocidrone_leaderboard(
        self,
        interaction: discord.Interaction,
        official: bool,
        race_mode: int,
        track_id: int,
        version: float,
    ):
        json_data = velocidrone_helper.get_leaderboard(
            f"https://www.velocidrone.com/leaderboard_as_json2/{official}/{race_mode}/{track_id}/{version}"
        )

        leaderboard_output = """"""

        for i in range(min(len(json_data[1]), 9), -1, -1):
            leaderboard_output += f"""\nLap Time, _{json_data[1][i]["lap_time"]}_:   **{json_data[1][i]["playername"]}**"""

        if len(leaderboard_output) == 0:
            leaderboard_output = "No one is on the leaderboard yet!"

        leaderboard_output = (
            f"""\nTrack: {json_data[0]["track_name"]}""" + leaderboard_output
        )

        await interaction.response.send_message(
            leaderboard_output,
            ephemeral=False,
            delete_after=config["leaderboard_delete_after_seconds"],
        )

    @app_commands.command(
        name="velocidrone_add_whitelist",
        description="Adds to the velocidrone whitelist",
    )
    async def velocidrone_add_whitelist(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        velocidrone_helper.whitelist_add(name)
        await interaction.response.send_message(
            f"Added **{name}** to the Velocidrone whitelist",
            ephemeral=True,
        )

    @app_commands.command(
        name="velocidrone_remove_whitelist",
        description="Removes to the velocidrone whitelist",
    )
    async def velocidrone_remove_whitelist(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        velocidrone_helper.whitelist_remove(name)
        await interaction.response.send_message(
            f"Removed **{name}** from the Velocidrone whitelist",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Velocidrone(bot))
