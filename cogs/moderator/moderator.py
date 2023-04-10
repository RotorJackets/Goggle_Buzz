import discord
from discord import app_commands
from discord.ext import commands


@app_commands.guild_only()
class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
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
