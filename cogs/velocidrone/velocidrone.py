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
        self.background_leaderboard_update.start()

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
            f"https://www.velocidrone.com/leaderboard_as_json2/{1 if official else 0}/{race_mode}/{track_id}/{version}"
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

    # TODO: Combine these two commands into one
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

    # TODO: Combine these two commands into one
    @app_commands.command(
        name="velocidrone_add_track_id",
        description="Adds to the velocidrone track_id",
    )
    async def velocidrone_add_track(
        self,
        interaction: discord.Interaction,
        official: bool,
        race_mode: int,
        track_id: int,
        version: float,
    ):
        track = velocidrone_helper.track_add(official, race_mode, track_id, version)
        if track is None:
            await interaction.response.send_message(
                f"**{track_id}** is already on the list!",
                ephemeral=True,
            )
            return
        else:
            await interaction.response.send_message(
                f"Added **{track_id}** to the Velocidrone track_id",
                ephemeral=True,
            )

    @app_commands.command(
        name="velocidrone_remove_track_id",
        description="Removes to the velocidrone track_id",
    )
    async def velocidrone_remove_track(
        self,
        interaction: discord.Interaction,
        track_id: int,
    ):
        track = velocidrone_helper.track_remove(track_id)
        if track is None:
            await interaction.response.send_message(
                f"**{track_id}** is not on the list!",
                ephemeral=True,
            )
            return
        else:
            await interaction.response.send_message(
                f"Removed **{track_id}** from the Velocidrone track_id",
                ephemeral=True,
            )

    @app_commands.command(
        name="velocidrone_track_list",
        description="Lists the tracks",
    )
    async def velocidrone_track_list(
        self,
        interaction: discord.Interaction,
    ):
        track_list = velocidrone_helper.get_track_list()

        track_output = """"""

        for track in track_list:
            track_output += f"""\n**{track}**"""

        if len(track_output) == 0:
            track_output = "No tracks are on the list yet!"

        await interaction.response.send_message(
            track_output,
            ephemeral=True,
        )

    @tasks.loop(seconds=config["track_update_interval"], count=None)
    async def background_leaderboard_update(self):
        track_diff = velocidrone_helper.track_update()
        if track_diff is not {}:
            for track in track_diff:
                message = """"""
                for pilot in track_diff[track].keys():
                    pilot_info = track_diff[track][pilot]
                    message += (
                        f"""\n**{pilot}** has set a _{"first" if pilot_info["first_time"] else "new"}_ """
                        + f"""time of **{pilot_info["lap_time"]}**!"""
                    )

                await self.bot.get_channel(config["leaderboard_channel_id"]).send(
                    embed=discord.Embed(
                        title=f"""**{track}** has a new leaderboard!""",
                        description=message,
                    )
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Velocidrone(bot))
