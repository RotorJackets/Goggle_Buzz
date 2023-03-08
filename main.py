import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from api_key import bot_token

# Version 1.0
# Testing Server id = 473695678690885632
# RotorJackets id = 723199784697200810

guilds = [discord.Object(id=473695678690885632), discord.Object(id=723199784697200810)]


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        # if not self.synced:
        #     await tree.sync()
        #     self.synced = True
        print(f"We have logged in as: {self.user}.")


bot = client()
tree = app_commands.CommandTree(bot)


# Commands
@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!sync" in message.content.lower():
        await message.channel.send("!sonc")
        await tree.sync()


@tree.command(name="test_input")
async def test_input(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(
        f"Modify {number=} {string=}", ephemeral=True
    )


@tree.command(name="test_options")
@app_commands.describe(option="This is a description of what the option means")
@app_commands.choices(
    option=[
        app_commands.Choice(name="Option 1", value="1"),
        app_commands.Choice(name="Option 2", value="2"),
    ]
)
async def test_options(interaction: discord.Interaction, option: app_commands.Choice[str]):
    pass


bot.run(bot_token)
