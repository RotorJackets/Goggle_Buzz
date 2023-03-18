import discord
from discord import app_commands
from discord.ext import commands
from config import config as config_main

config = config_main["util"]


@app_commands.guild_only()
class JoinMessage(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(config["welcome_channel"])
        pfp = member.avatar
        join_embed = discord.Embed(
            title="Welcome to RotorJackets!",
            description=f"{member.mention} has joined the server!",
            color=discord.Color.gold(),
        )
        join_embed.set_author(name=f"{member.name}", icon_url=(pfp))
        join_embed.set_thumbnail(url=(pfp))
        await channel.send(embed=join_embed)
        embed = discord.Embed(
            title="Welcome to the server!",
            description=f"""
Feel free to throw something in the Introductions channel so we can get to know you. We welcome everyone to our club! Even if you know nothing about drones, we are glad to help you so feel free to ask any question any time!

Check out <#{config["new_member_info_channel"]}> for some helpful tips
You can ask questions in <#{config["build_help_channel"]}> 
Introductions are in <#{config["introductions_channel"]}>

If you are a Georgia Tech student, please become a member on engage.gatech.edu and join the club there. https://gatech.campuslabs.com/engage/organization/rotorjackets
""",
            color=discord.Color.gold(),
        )

        await member.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(JoinMessage(bot))
