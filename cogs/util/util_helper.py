import asyncio
import itertools
import time
import json
import requests
import discord
from config import config as config_main

config = config_main["util"]


def setup(guilds: list[discord.guild.Guild]):
    tempDict = {}

    try:
        with open(config["save_location"] + "util.json") as f:
            pass
        f.close()
    except IOError as e:
        print("Util save file not found . . . Making that shit!")
        f = open(config["save_location"] + "util.json", "w")
        f.write('{"guilds": {}}')
        f.close()

    with open(config["save_location"] + "util.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for guild in guilds:
        if (guild_id := str(guild.id)) not in config.keys():
            config["guilds"][guild_id] = {
                "welcome_channel": None,
            }

    save_config()


def save_config():
    tempDict = {}

    for guild in list(config["guilds"].keys()):
        tempDict["guilds"][guild] = config[guild]

    with open(config["save_location"] + "util.json", "w") as f:
        json.dump(tempDict, f)


def set_channel(guild_id: int, name: str, channel: discord.TextChannel):
    config[str(guild_id)][name] = channel
    save_config()
