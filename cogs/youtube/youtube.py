import discord
import json
from discord import app_commands
from discord.ext import commands
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

        result = youtube_helper.add_channel(interaction.guild.id, channel)
        if result:
            await interaction.response.send_message(f"Now tracking {channel}")
        else:
            await interaction.response.send_message(
                f"Failed to track {channel}", ephemeral=True
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

        result = youtube_helper.remove_channel(interaction.guild.id, channel)
        await interaction.response.send_message(f"Stopped tracking {channel}")

    @app_commands.command(
        name="list_channels",
        description="Lists the current guild's tracked channels",
    )
    async def list_channels(
        self,
        interaction: discord.Interaction,
    ):
        channel_list = youtube_helper.get_guild_channels(interaction.guild.id)

        channel_output = """"""

        for channel in channel_list:
            channel_output += f"""\n**`{channel}**"""

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
        youtube_helper.whitelist_guild(interaction.guild, whitelist)
        await interaction.response.send_message(
            f"Guild **{interaction.guild.name}** is whitelisted: *{whitelist}*",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YouTube(bot))
