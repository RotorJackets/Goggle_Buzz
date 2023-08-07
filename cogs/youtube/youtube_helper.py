import asyncio
import itertools
import time
import json
import requests
import discord
from config import config as config_main

config = config_main["YouTube"]


def setup(guilds: list[discord.guild.Guild]):
    tempDict = {}

    try:
        with open(config["save_location"] + "util.json") as f:
            pass
        f.close()
    except IOError as e:
        print("YouTube save file not found . . . Making that shit!")
        f = open(config["save_location"] + "youtube.json", "w")
        f.write('{"guilds":{}}')
        f.close()

    with open(config["save_location"] + "youtube.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for guild in guilds:
        if (guild_id := str(guild.id)) not in config["guilds"].keys():
            config["guilds"][guild_id] = {"whitelisted": False, "tracked_channels": {}}

    save_config()


def save_config():
    tempDict = {}

    tempDict["guilds"] = config["guilds"]

    with open(config["save_location"] + "youtube.json", "w") as f:
        json.dump(tempDict, f)


def add_channel(guild_id: int, channel: str):
    if channel in config["guilds"][str(guild_id)]["tracked_channels"].keys():
        return True

    if check_channel_existence():
        config["guilds"][str(guild_id)]["tracked_channels"][channel] = {
            "last_updated": time.time()
        }
        save_config()
        return True
    else:
        return False


def remove_channel(guild_id: int, channel: str) -> bool:
    if channel not in config["guilds"][str(guild_id)]["tracked_channels"].keys():
        return True

    config["guilds"][str(guild_id)]["tracked_channels"].remove(channel)
    return True


def get_guild_channels(guild_id: int) -> list[str]:
    return list(config["guilds"][str(guild_id)]["tracked_channels"].keys())


def get_all_channels() -> list[str]:
    channel_list = set()

    for guild in config["guilds"]:
        for channel in guild["tracked_channels"]:
            channel_list.add(channel)

    return channel_list


def get_all_channel_count() -> int:
    return len(get_all_channels())


def check_channel_existence(channel: str) -> bool:
    return True


def set_channel(guild_id: int, name: str, channel: discord.TextChannel):
    config["guilds"][str(guild_id)]["notification_channel"] = channel
    save_config()
