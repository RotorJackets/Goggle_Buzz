import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import cogs.util.util_helper as util_helper
from config import config as config_main

config = config_main["util"]


@app_commands.guild_only()
class UtilSetup(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        util_helper.setup(self.bot.guilds)
        print("Util has been setup")

    @app_commands.command(
        name="set_welcome_channel",
        description="Sets the welcome channel",
    )
    async def set_leaderboard_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
    ):
        role = get(interaction.guild.roles, name=config["util_edit_role"])
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                f"""You must have the **{config["util_edit_role"]}** role to use this command""",
                ephemeral=True,
            )
            return

        util_helper.set_channel(interaction.guild.id, "welcome_channel", channel.id)
        await interaction.response.send_message(
            f"Set the leaderboard channel to {channel.mention}",
            ephemeral=False,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UtilSetup(bot))
