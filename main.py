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

guilds = []

for i in config["guilds"]:
    guilds.append(discord.Object(id=i))


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

    if (
        "!sync" in message.content.lower()
        and message.author.guild_permissions.administrator
    ):
        print("Starting sync.")
        await tree.sync()
        await message.channel.send("Synced")
        print("Command tree synced.")

    if (
        "!save" in message.content.lower()
        and message.author.guild_permissions.administrator
    ):
        leaderboard.save()
        await message.channel.send("Saved")

    if (
        level := leaderboard.adjust_xp(message.guild.id, message.author.id, 1)
    ) is not None:
        await message.channel.send(
            f"{message.author.mention} has leveled up to level {level}"
        )


@tree.command(name="show_leaderboard", description="Shows the leaderboard")
async def show_leaderboard(interaction: discord.Interaction):
    leaders = leaderboard.get_leaders(interaction.guild.id)
    leaderboard_output = """"""

    for i in range(len(leaders)):
        leaderboard_output += f"""\nLevel {leaders[i][1]["level"]}:   {await bot_client.fetch_user(leaders[i][0])}"""

    await interaction.response.send_message(
        leaderboard_output,
        ephemeral=False,
        delete_after=config["leaderboard_delete_after_seconds"],
    )


@tree.command(
    name="show_level", description="Shows your level or the level of another user"
)
@app_commands.describe(member="The user to show the level of, defaults to yourself")
async def show_level(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    member_info = leaderboard.get_info(interaction.guild.id, member.id)
    await interaction.response.send_message(
        f"""**{member.mention}** is in **{member_info["place"]}** place on the leaderboard! """
        + f"""They are level **{member_info["level"]}** and are """
        + f"""**{member_info["xp"]/config["level_up_XP"] * 100:3.2f}%** to the next level!""",
        ephemeral=True,
    )


@tree.command(name="fight_song", description="Sends a random fight song quote")
async def fight_song(interaction: discord.Interaction):
    await interaction.response.send_message(
        random.choice(config["fight_song_quotes"]), ephemeral=False
    )


# Moderator Commands
@tree.command(name="kick", description="Kicks a user")
@commands.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction, member: discord.Member, reason: str = None
):
    await interaction.response.send_message(
        f"""{member.mention} has been kicked.""", ephemeral=True
    )
    await member.kick(reason=reason)


@tree.command(name="ban", description="Bans a user")
@commands.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction, member: discord.Member, reason: str = None
):
    await interaction.response.send_message(
        f"""{member.mention} has been banned.""", ephemeral=True
    )
    await member.ban(reason=reason)


@tree.command(name="change_nick", description="Changes a user's nickname")
@commands.has_permissions(manage_nicknames=True)
async def change_nick(
    interaction: discord.Interaction, member: discord.Member, nick: str = None
):
    await interaction.response.send_message(
        f"""{member.mention}'s nickname has been changed to {nick}.""", ephemeral=True
    )
    await member.edit(nick=nick)


bot_client.run(bot_token)
