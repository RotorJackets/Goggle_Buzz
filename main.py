'''
'''
import discord
import random
from discord import app_commands
from discord.utils import get
from api_key import bot_token

# Version 1.0
# Testing Server id = 473695678690885632
# RotorJackets id = 723199784697200810

guilds = [discord.Object(id = 473695678690885632), discord.Object(id =723199784697200810)]

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"We have logged in as: {self.user}.")


bot = client()
tree = app_commands.CommandTree(bot)


# Commands
@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!sync" in message.content.lower():
        await tree.sync()
        await message.channel.send("Synced")
        print("Command tree synced.")

bot.run(bot_token)
