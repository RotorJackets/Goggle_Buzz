import discord
import json
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
import cogs.youtube.youtube_helper as youtube_helper

from config import config as config_main

config = config_main["youtube"]


class YouTube(commands.GroupCog, name="youtube"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        youtube_helper.setup(self.bot.guilds)
        self.background_channel_update.start()
        print("YouTube has been setup")

    @app_commands.command(
        name="set_notification_channel", description="Sets the notification channel"
    )
    async def set_notification_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        role = get(interaction.guild.roles, name=config["youtube_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["youtube_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        youtube_helper.set_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(
            f"Set the notification channel to {channel.mention}",
            ephemeral=False,
        )

    @app_commands.command(
        name="add_channel", description="Adds a channel to your notification channel"
    )
    async def add_channel(self, interaction: discord.Interaction, channel: str):
        role = get(interaction.guild.roles, name=config["youtube_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["youtube_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        result = youtube_helper.add_channel(interaction.guild.id, channel.lower())
        if result:
            await interaction.response.send_message(f"Now tracking {channel}")
        else:
            await interaction.response.send_message(
                f"Failed to track **{channel}**", ephemeral=True
            )

    @app_commands.command(
        name="remove_channel",
        description="Removes a channel to your notification channel",
    )
    async def remove_channel(self, interaction: discord.Interaction, channel: str):
        role = get(interaction.guild.roles, name=config["youtube_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["youtube_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        result = youtube_helper.remove_channel(interaction.guild.id, channel.lower())
        await interaction.response.send_message(f"Stopped tracking {channel}")

    @app_commands.command(
        name="list_channels",
        description="Lists the current guild's tracked channels",
    )
    async def list_channels(
        self,
        interaction: discord.Interaction,
    ):
        # TODO: Make this an embed
        channel_list = youtube_helper.get_guild_channels(interaction.guild.id)

        channel_output = """"""

        for channel in channel_list:
            channel_output += f"""\n**{channel}**"""

        if len(channel_output) == 0:
            channel_output = "No channels are being tracked yet!"

        await interaction.response.send_message(
            channel_output,
            ephemeral=False,
        )

    @app_commands.command(
        name="whitelist_guild",
        description="Whitelists the guild",
    )
    @commands.has_permissions(administrator=True)
    async def whitelist_guild(self, interaction: discord.Interaction, whitelist: bool):
        youtube_helper.whitelist_guild(interaction.guild.id, whitelist)
        await interaction.response.send_message(
            f"Guild **{interaction.guild.name}** is whitelisted: *{whitelist}*",
            ephemeral=True,
        )

    @app_commands.command(
        name="get_latest_video",
        description="Gets the latest video from a channel",
    )
    async def get_latest_video(
        self,
        interaction: discord.Interaction,
        channel: str,
    ):
        video = youtube_helper.get_latest_channel_data(channel.lower())
        if video is None:
            await interaction.response.send_message(
                f"Failed to get the latest video from **{channel}**",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"""Here is the latest video from **{channel}**:\n{video["url"]}""",
            ephemeral=False,
        )

    @tasks.loop(
        seconds=config["channel_update_interval"],
        count=None,
    )
    async def background_channel_update(self):
        YouTube.background_channel_update.change_interval(
            seconds=(youtube_helper.get_all_channel_count() * 30) + 10
        )

        channel_diff = await youtube_helper.get_all_channel_diff()

        for guild in self.bot.guilds:
            if not youtube_helper.is_guild_whitelisted(guild.id):
                continue

            channel_id = youtube_helper.get_guild_notification_channel(guild.id)
            if channel_id is None:
                print(f"Guild {guild.name} has no channel set for YouTube")
                continue

            for channel in channel_diff.keys():
                if channel not in youtube_helper.get_guild_channels(guild.id):
                    continue

                await self.bot.get_channel(channel_id).send(
                    f'**{channel}** has a new video:\n{channel_diff[channel]["url"]}'
                )

        youtube_helper.save_config()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YouTube(bot))
