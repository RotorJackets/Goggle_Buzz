import asyncio
import itertools
import time
import json
import requests
import re
import discord

from config import config as config_main

config = config_main["youtube"]


def setup(guilds: list[discord.guild.Guild]):
    tempDict = {}

    try:
        with open(config["save_location"] + "youtube.json") as f:
            pass
        f.close()
    except IOError as e:
        print("YouTube save file not found . . . Making that shit!")
        f = open(config["save_location"] + "youtube.json", "w")
        f.write('{"channels":{}, "guilds":{}}')
        f.close()

    with open(config["save_location"] + "youtube.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for guild in guilds:
        if (guild_id := str(guild.id)) not in config["guilds"].keys():
            config["guilds"][guild_id] = {"whitelisted": False, "tracked_channels": []}

    save_config()


def save_config():
    tempDict = {}

    tempDict["channels"] = config["channels"]
    tempDict["guilds"] = config["guilds"]

    with open(config["save_location"] + "youtube.json", "w") as f:
        json.dump(tempDict, f)


def add_channel(guild_id: int, channel: str):
    if channel in config["guilds"][str(guild_id)]["tracked_channels"]:
        return True

    if check_channel_existence(channel):
        config["guilds"][str(guild_id)]["tracked_channels"].append(channel)
        if channel not in config["channels"].keys():
            config["channels"][channel] = {
                "latest_video": {"info": None, "url": None},
                "last_updated": None,
            }
        save_config()
        return True
    else:
        return False


def remove_channel(guild_id: int, channel: str):
    if channel not in config["guilds"][str(guild_id)]["tracked_channels"]:
        return

    config["guilds"][str(guild_id)]["tracked_channels"].remove(channel)

    if channel not in get_all_channels():
        del config["channels"][channel]

    save_config()


def get_guild_channels(guild_id: int) -> list[str]:
    return config["guilds"][str(guild_id)]["tracked_channels"]


def get_all_channels() -> list[str]:
    channel_list = set()

    for guild in config["guilds"].keys():
        for channel in config["guilds"][guild]["tracked_channels"]:
            channel_list.add(channel)

    return list(channel_list)


def get_all_channel_count() -> int:
    return len(config["channels"].keys())


def check_channel_existence(channel: str) -> dict[str, str] | None:
    """Checks if a channel exists and returns the latest video info and url if it does.

    Args:
        channel (str): The channel to check.

    Returns:
        dict[str, str] | None: A dictionary containing the latest video info and url for a given channel, or None if the channel does not exist.
    """
    channel_data = get_channel_data(channel)

    if channel_data is None:
        return None
    else:
        return channel_data


def whitelist_guild(guild_id: int, whitelist: bool):
    config["guilds"][str(guild_id)]["whitelisted"] = whitelist

    save_config()


def set_channel(guild_id: int, channel: discord.TextChannel):
    config["guilds"][str(guild_id)]["notification_channel"] = channel
    save_config()


def get_channel_data(channel: str) -> dict[str, str]:
    """Returns a dictionary containing the latest video info and url for a given channel.

    Args:
        channel (str): The channel to get the data for.

    Returns:
        dict[str, str]: A dictionary containing the latest video info and url for a given channel.
        >>> {"info": info, "url": url}
    """

    channel_url = "https://www.youtube.com/@" + channel

    html = requests.get(channel_url + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    url = (
        "https://www.youtube.com/watch?v="
        + re.search('(?<="videoId":").*?(?=")', html).group()
    )

    return {"info": info, "url": url}


def update_channel_data(
    channel: str, channel_data: dict[str, str]
) -> dict[str, str] | None | bool:
    """Updates the latest video info and url for a given channel.

    Args:
        channel (str): The channel to update the data for.

    Returns:
        dict[str, str] | None | false \n
        A dictionary containing the latest video info and url for a given channel, \n
        or None if the channel does not exist, \n
        or is not in json, or False if the data is the same.
    """
    if channel_data is None and channel not in config["channels"].keys():
        return None

    if config["channels"][channel]["latest_video"]["url"] == channel_data["url"]:
        return False

    config["channels"][channel]["latest_video"]["info"] = channel_data["info"]
    config["channels"][channel]["latest_video"]["url"] = channel_data["url"]
    config["channels"][channel]["last_updated"] = time.time()
    save_config()
    return channel_data


def get_latest_channel_data(channel: str) -> dict[str, str] | None:
    """Returns the latest video info and url for a given channel.

    Args:
        channel (str): The channel to get the data for.

    Returns:
        dict[str, str] | None: A dictionary containing the latest video info and url for a given channel, or None if the channel does not exist.
    """
    channel_data = check_channel_existence(channel)

    if channel_data is None:
        return None

    return channel_data


async def get_all_channel_diff() -> dict[str, dict[str, str]]:
    """Returns a dictionary containing the latest video info and url for all channels that have been updated.

    Returns:
        dict[str, dict[str, str]]: A dictionary containing the latest video info and url for all channels that have been updated.
        >>> {"channel": {"info": info, "url": url}}
    """
    channel_diff = {}
    for channel in list(config["channels"].keys()):
        await asyncio.sleep(30)
        new_content = update_channel_data(channel, get_channel_data(channel))
        if new_content:
            channel_diff[channel] = new_content

    return channel_diff


def is_guild_whitelisted(guild_id: int) -> bool:
    return config["guilds"][str(guild_id)]["whitelisted"]


def get_guild_notification_channel(guild_id: int) -> int:
    return config["guilds"][str(guild_id)]["notification_channel"]


if __name__ == "__main__":
    pass
