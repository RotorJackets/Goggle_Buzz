import discord
from discord import app_commands
from discord.ext import commands
import lib.leaderboard as leaderboard
from lib.config import config


class Leaderboard(commands.Cog):
    def __init__(self, bot_client: discord.Client):
        self.bot_client = bot_client
        self._last_member = None

    @app_commands.command(
        name="show_leaderboard",
        description="Shows the leaderboard",
    )
    async def show_leaderboard(self, interaction: discord.Interaction) -> None:
        leaders = leaderboard.get_leaders(interaction.guild)
        leaderboard_output = """"""

        for i in range(len(leaders)):
            leaderboard_output += f"""\nLevel {leaders[i][1]["level"]}:   {await self.bot_client.fetch_user(leaders[i][0])}"""

        if len(leaderboard_output) == 0:
            leaderboard_output = "No one is on the leaderboard yet!"

        await interaction.response.send_message(
            leaderboard_output,
            ephemeral=False,
            delete_after=config["leaderboard_delete_after_seconds"],
        )

    @app_commands.command(
        name="show_level",
        description="Shows your level or the level of another user",
    )
    @app_commands.describe(member="The user to show the level of, defaults to yourself")
    async def show_level(
        self, interaction: discord.Interaction, member: discord.Member = None
    ) -> None:
        if member is None:
            member = interaction.user

        member_info = leaderboard.get_info(interaction.guild, member)
        await interaction.response.send_message(
            f"""**{member.mention}** is in **{member_info["place"]}** place on the leaderboard! """
            + f"""They are level **{member_info["level"]}** and are """
            + f"""**{member_info["xp"]/config["level_up_XP"] * 100:3.2f}%** to the next level!""",
            ephemeral=True,
        )

    @app_commands.command(
        name="save_leaderboard",
        description="Saves the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def save_leaderboard(self, interaction: discord.Interaction) -> None:
        leaderboard.save(interaction.guild)
        await interaction.response.send_message(
            f"Leaderboard for **{interaction.guild.name}** has been saved.",
            ephemeral=True,
        )

    @app_commands.command(
        name="reset_leaderboard",
        description="Resets the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def reset_leaderboard(self, interaction: discord.Interaction) -> None:
        leaderboard.reset_guild(interaction.guild)
        await interaction.response.send_message(
            f"Leaderboard for **{interaction.guild.name}** has been reset.",
            ephemeral=True,
        )

    @app_commands.command(
        name="reset_member_xp",
        description="Resets the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def reset_member_xp(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        leaderboard.reset_member(member)
        await interaction.response.send_message(
            f"Leaderboard for **{interaction.guild.name}** has been reset.",
            ephemeral=True,
        )


def setup(bot_client: discord.Client):
    bot_client.add_cog(Leaderboard(bot_client))
