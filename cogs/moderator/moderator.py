import discord
from discord import app_commands
from discord.ext import commands


class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="kick",
        description="Kicks a user",
    )
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        await interaction.response.send_message(
            f"""{member.mention} has been kicked.""", ephemeral=True
        )
        await member.kick(reason=reason)

    @app_commands.command(
        name="ban",
        description="Bans a user",
    )
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        await interaction.response.send_message(
            f"""{member.mention} has been banned.""", ephemeral=True
        )
        await member.ban(reason=reason)

    @app_commands.command(
        name="change_nick",
        description="Changes a user's nickname",
    )
    @commands.has_permissions(manage_nicknames=True)
    async def change_nick(
        self, interaction: discord.Interaction, member: discord.Member, nick: str = None
    ):
        await interaction.response.send_message(
            f"""{member.mention}'s nickname has been changed to {nick}.""",
            ephemeral=True,
        )
        await member.edit(nick=nick)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderator(bot))
