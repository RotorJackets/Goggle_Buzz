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
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync( guild= discord.Object(id = 473695678690885632))
            self.synced = True
        print(f"We have logged in as: {self.user}.")
        
bot = client()
tree = app_commands.CommandTree(bot)

#Commands
@tree.command(name = "flyday", description = "Find the next fly day", guilds= guilds)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Salt reloaded. It's time to be a fucking menace.")

bot.run(bot_token)