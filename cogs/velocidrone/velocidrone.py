import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
from discord.utils import get

import cogs.velocidrone.velocidrone_helper as velocidrone_helper
from config import config as config_main

config = config_main["velocidrone"]


class Removal(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
    remove : bool = None
    @discord.ui.button(label="Remove",
                       style=discord.ButtonStyle.danger,
                       custom_id="remove")
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.remove = True
        button.disabled = True
        button1 = [i for i in self.children if i.custom_id=="cancel"][0]
        button1.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
    @discord.ui.button(label="Cancel",
                       style=discord.ButtonStyle.grey,
                       custom_id="cancel")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.remove = False
        button.disabled = True
        button1 = [i for i in self.children if i.custom_id == "remove"][0]
        button1.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    async def on_timeout(self):
        button = [i for i in self.children if i.custom_id == "remove"][0]
        button.disabled = True
        button = [i for i in self.children if i.custom_id == "cancel"][0]
        button.disabled = True
        await self.message.edit(view=self)
@app_commands.guild_only()
class Velocidrone(commands.GroupCog, name="velocidrone"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()


    @commands.Cog.listener()
    async def on_ready(self):
        velocidrone_helper.setup()
        self.background_leaderboard_update.start()

    @app_commands.command(
        name="leaderboard",
        description="Shows the leaderboard for a specific track",
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        track_id: int,
    ):
        json_data = velocidrone_helper.get_leaderboard_guild(
            interaction.guild.id,
            f"https://www.velocidrone.com/leaderboard_as_json2/{0}/{6}/{track_id}/{1.16}",
        )

        leaderboard_output = """"""

        for i in range(min(len(json_data[1]) - 1, 9), -1, -1):
            leaderboard_output += f"""\nLap Time, _{json_data[1][i]["lap_time"]}_:   **{json_data[1][i]["playername"]}**"""

        if len(leaderboard_output) == 0:
            leaderboard_output = "\nNo one is on the leaderboard yet!"

        leaderboard_output = (
            f"""\nTrack: {json_data[0]["track_name"]}""" + leaderboard_output
        )

        await interaction.response.send_message(
            leaderboard_output,
            ephemeral=False,
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

        velocidrone_helper.whitelist_add_guild(interaction.guild.id, name)
        await interaction.response.send_message(
            f"Added **{name}** to the Velocidrone whitelist",
            ephemeral=False,
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

        view = Removal()
        await interaction.response.send_message(
            content=f"Are you sure you want to remove **{name}** from the Velocidrone whitelist?",
            view=view,
        )

        message = await interaction.original_response()
        view.message = message
        timeout = await view.wait()

        if timeout is True:
            await message.edit(content=f"Timed out")
        elif view.remove is True:
            velocidrone_helper.whitelist_remove_guild(interaction.guild.id, name)
            await message.edit(
                content=f"Removed **{name}** from the Velocidrone whitelist",
            )
        elif view.remove is False:
            await message.edit(
                content="Cancelled",
            )

    @app_commands.command(
        name="add_track",
        description="Adds to the velocidrone tracks",
    )
    async def add_track(
        self,
        interaction: discord.Interaction,
        leaderboard_url: str,
    ):
        track_id = int(leaderboard_url.split("/")[-2])

        role = get(interaction.guild.roles, name=config["velocidrone_edit_role"])

        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["velocidrone_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        track = velocidrone_helper.track_add_guild(interaction.guild.id, track_id)
        if track is None:
            await interaction.response.send_message(
                f"**{track_id}** does not exist!",
                ephemeral=True,
            )
            return
        else:
            await interaction.response.defer(ephemeral=True, thinking=True)

            await asyncio.sleep(3)

            track_url = velocidrone_helper.get_leaderboard_url(track_id)

            await interaction.followup.send(
                content=None,
                embed=discord.Embed(
                    title=f"**{track}**",
                    description=f"Added _{track}_ to the Velocidrone list\nTrack ID: {track_id}",
                    color=discord.Color.green(),
                    url=track_url,
                ),
                ephemeral=False,
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
        view = Removal()
        await interaction.response.send_message(
            content=f"Are you sure you want to remove Track ID: **{track_id}** from the Velocidrone track list?",
            view=view,
        )

        message = await interaction.original_response()
        view.message = message
        timeout = await view.wait()

        if timeout is True:
            await message.edit(content=f"Timed out")
        elif view.remove is True:
            track = velocidrone_helper.track_remove_guild(interaction.guild.id, track_id)
            if track is None:
                await message.edit(
                    content=f"**{track}** is not on the list!",
                )
                return
            else:
                await message.edit(
                    content=f"Removed **{track}** from the Velocidrone track_id",
                )
        elif view.remove is False:
            await message.edit(
                content="Cancelled",
            )

    @app_commands.command(
        name="list_tracks",
        description="Lists the tracks",
    )
    async def list_tracks(
        self,
        interaction: discord.Interaction,
    ):
        track_list = velocidrone_helper.get_track_list_guild(interaction.guild.id)

        track_output = """"""

        for track in track_list:
            track_output += f"""\n**{track}**"""

        if len(track_output) == 0:
            track_output = "No tracks are on the list yet!"

        await interaction.response.send_message(
            track_output,
            ephemeral=False,
        )

    @tasks.loop(
        seconds=config["track_update_interval"],
        count=None,
    )
    async def background_leaderboard_update(self):
        Velocidrone.background_leaderboard_update.change_interval(
            seconds=(velocidrone_helper.get_number_of_tracks() * 10) + 30
        )

        track_diff = await velocidrone_helper.track_update()

        if track_diff is not {}:
            for guild_id in config["leaderboard_guilds"]:
                for track_id in track_diff:
                    if track_id not in velocidrone_helper.get_guild_track_list(
                        guild_id
                    ):
                        continue

                    message = """"""
                    for pilot in track_diff[track_id].keys():
                        if pilot not in velocidrone_helper.get_guild_whitelist(
                            guild_id
                        ):
                            continue

                        pilot_info = track_diff[track_id][pilot]
                        message += (
                            f"""\n**{pilot}** has set a _{"first" if pilot_info["first_time"] else "new"}_ """
                            + f"""time of **{pilot_info["lap_time"]}**!"""
                        )

                    track = velocidrone_helper.get_track(track_id)
                    if message != """""":
                        await self.bot.get_channel(
                            velocidrone_helper.get_guild_leaderboard_channel(guild_id)
                        ).send(
                            embed=discord.Embed(
                                title=f"""**{track[0]["track_name"]}** has a new leaderboard!""",
                                description=message,
                                url=velocidrone_helper.get_leaderboard_url(track_id),
                                timestamp=datetime.datetime.now(),
                                color=discord.Color.gold(),
                            )
                        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Velocidrone(bot))
