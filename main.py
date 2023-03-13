import discord
import random
from discord.ext import commands, tasks
from discord import app_commands
from discord.utils import get
from api_key import bot_token

import lib.leaderboard as leaderboard
from lib.config import config

# Version 1.0
# Testing Server id = 473695678690885632
# RotorJackets id = 723199784697200810

guilds = [discord.Object(id=473695678690885632), discord.Object(id=723199784697200810)]


class bot_client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        await self.wait_until_ready()
        background_leaderboard_save.start()
        print(f"We have logged in as: {self.user}.")


bot_client = bot_client()
tree = app_commands.CommandTree(bot_client)


# Loops
@tasks.loop(seconds=config["leaderboard_save_interval_seconds"], count=None)
async def background_leaderboard_save():
    leaderboard.save()


# Commands

# @tree.command(name="test_input")
# async def test_input(interaction: discord.Interaction, number: int, string: str):
#     await interaction.response.send_message(
#         f"Modify {number=} {string=}", ephemeral=True
#     )


# @tree.command(name="test_options")
# @app_commands.describe(option="This is a description of what the option means")
# @app_commands.choices(
#     option=[
#         app_commands.Choice(name="Option 1", value="1"),
#         app_commands.Choice(name="Option 2", value="2"),
#     ]
# )
# async def test_options(
#     interaction: discord.Interaction, option: app_commands.Choice[str]
# ):
#     pass


@bot_client.event
async def on_message(message):
    if message.author.bot:
        return

    if "!sync" in message.content.lower():
        print("Starting sync.")
        await tree.sync()
        await message.channel.send("Synced")
        print("Command tree synced.")
    
    if "!save" in message.content.lower():
        leaderboard.save()
        await message.channel.send("Saved")

    if (level := leaderboard.adjust_xp(message.guild.id, message.author.id, 1)) is not None:
        await message.channel.send(
            f"{message.author.mention} has leveled up to level {level}"
        )


@tree.command(name="show_leaderboard")
async def show_leaderboard(interaction: discord.Interaction):
    leaders = leaderboard.get_leaders()
    leaderboard_output = """"""

    for i in range(len(leaders)):
        leaderboard_output += f"""
Level {leaders[i][1]["level"]}:   {await bot_client.fetch_user(leaders[i][0])}"""

    await interaction.response.send_message(
        leaderboard_output,
        ephemeral=False,
        delete_after=config["leaderboard_delete_after_seconds"],
    )


@tree.command(name="fight_song")
async def fight_song(interaction: discord.Interaction):
    await interaction.response.send_message(
        random.choice(config["fight_song_quotes"]), ephemeral=False
    )


bot_client.run(bot_token)
