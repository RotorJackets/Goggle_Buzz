import discord
import random
from discord.ext import commands, tasks
from discord import app_commands
from discord.utils import get
from api_key import bot_token

import lib.leaderboard as leaderboard
from lib.config import config

from cogs.leaderboard import Leaderboard_cog as Leaderboard_cog

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

    async def setup_hook(self):
        await bot_client.load_extension(Leaderboard_cog)


bot_client = bot_client()
tree = app_commands.CommandTree(bot_client)


# Loops
@tasks.loop(seconds=config["leaderboard_save_interval_seconds"], count=None)
async def background_leaderboard_save() -> None:
    leaderboard.save(guilds)


# Commands
## Text Commands and Events
@bot_client.event
async def on_message(message) -> None:
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
        leaderboard.save(message.guild)
        await message.channel.send("Saved")

    if (level := leaderboard.adjust_xp(message.guild, message.author)) is not None:
        await message.channel.send(
            f"{message.author.mention} has leveled up to level {level}"
        )


@bot_client.event
async def on_member_join(member) -> None:
    pass


@bot_client.event
async def on_member_remove(member) -> None:
    pass


@bot_client.event
async def on_reaction_add(reaction, user) -> None:
    pass


@bot_client.event
async def on_reaction_remove(reaction, user) -> None:
    pass


@bot_client.event
async def on_reaction_clear(message, reactions) -> None:
    pass


## Fun Commands
@tree.command(
    name="fight_song",
    description="Sends a random fight song quote",
)
async def fight_song(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        random.choice(config["fight_song_quotes"]), ephemeral=False
    )


## Moderator Commands
@tree.command(
    name="kick",
    description="Kicks a user",
)
@commands.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction, member: discord.Member, reason: str = None
) -> None:
    await interaction.response.send_message(
        f"""{member.mention} has been kicked.""", ephemeral=True
    )
    await member.kick(reason=reason)


@tree.command(
    name="ban",
    description="Bans a user",
)
@commands.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction, member: discord.Member, reason: str = None
) -> None:
    await interaction.response.send_message(
        f"""{member.mention} has been banned.""", ephemeral=True
    )
    await member.ban(reason=reason)


@tree.command(
    name="change_nick",
    description="Changes a user's nickname",
)
@commands.has_permissions(manage_nicknames=True)
async def change_nick(
    interaction: discord.Interaction, member: discord.Member, nick: str = None
) -> None:
    await interaction.response.send_message(
        f"""{member.mention}'s nickname has been changed to {nick}.""", ephemeral=True
    )
    await member.edit(nick=nick)


bot_client.run(bot_token)
