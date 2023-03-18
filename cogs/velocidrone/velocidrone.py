import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
from discord.utils import get

import cogs.velocidrone.velocidrone_helper as velocidrone_helper
from config import config as config_main

config = config_main["velocidrone"]


class Velocidrone(commands.GroupCog, name="velocidrone"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    async def on_ready(self):
        velocidrone_helper.setup()
        self.background_leaderboard_update.start()

    @app_commands.command(
        name="leaderboard",
        description="Shows the leaderboard",
    )
    async def leaderboard(
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

    @app_commands.command(
        name="add_whitelist",
        description="Adds to the velocidrone whitelist",
    )
    async def add_whitelist(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        role = get(interaction.guild.roles, name=config["velocidrone_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["velocidrone_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        velocidrone_helper.whitelist_add(name)
        await interaction.response.send_message(
            f"Added **{name}** to the Velocidrone whitelist",
            ephemeral=True,
        )

    @app_commands.command(
        name="remove_whitelist",
        description="Removes to the velocidrone whitelist",
    )
    async def remove_whitelist(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        role = get(interaction.guild.roles, name=config["velocidrone_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["velocidrone_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        velocidrone_helper.whitelist_remove(name)
        await interaction.response.send_message(
            f"Removed **{name}** from the Velocidrone whitelist",
            ephemeral=True,
        )

    @app_commands.command(
        name="add_track",
        description="Adds to the velocidrone tracks",
    )
    async def add_track(
        self,
        interaction: discord.Interaction,
        official: bool,
        race_mode: int,
        track_id: int,
        version: float,
    ):
        # TODO: Make race_mode an option instead of an int
        role = get(interaction.guild.roles, name=config["velocidrone_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["velocidrone_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

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
        name="remove_track",
        description="Removes to the velocidrone tracks",
    )
    async def remove_track(
        self,
        interaction: discord.Interaction,
        track_id: int,
    ):
        role = get(interaction.guild.roles, name=config["velocidrone_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["velocidrone_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

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
        name="list_tracks",
        description="Lists the tracks",
    )
    async def list_tracks(
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
                        # TODO: Make this link to the leaderboard
                        url="https://www.velocidrone.com",
                        timestamp=datetime.datetime.now(),
                        color=discord.Color.gold(),
                    )
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Velocidrone(bot))
