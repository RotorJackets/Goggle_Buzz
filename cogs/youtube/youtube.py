import discord
import random

from discord import app_commands
from discord.ext import commands

class YouTube(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YouTube(bot))
