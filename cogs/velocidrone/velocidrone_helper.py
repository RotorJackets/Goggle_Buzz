import asyncio
import itertools
import time
import json
import requests

from config import config as config_main

config = config_main["velocidrone"]

debug = False

track_scenes = {
    "Apartment": 52,
    "Bando": 30,
    "Basketball Stadium": 29,
    "Castle Sneznik": 35,
    "City": 24,
    "Coastal": 22,
    "Combat Practice": 46,
    "Construction": 47,
    "Countryside": 12,
    "Drift Track": 48,
    "Dynamic Weather": 33,
    "DynamicPoly": 44,
    "Empty PolyWorld": 42,
    "Empty Scene Day": 16,
    "Empty Scene Night": 17,
    "Factory": 56,
    "Football Stadium": 8,
    "Future Hangar": 40,
    "Future Hangar Empty": 43,
    "House": 39,
    "Indoor GoKart": 31,
    "Industrial Wasteland": 7,
    "Island": 41,
    "Karting Track": 14,
    "La Mothe": 34,
    "Large Carpark": 26,
    "Library": 37,
    "MiniWarehouse": 51,
    "NEC Birmingham": 18,
    "Night Factory 2": 55,
    "NightClub": 38,
    "Office": 53,
    "Office Complex": 54,
    "PolyBando": 101,
    "PolyPort": 100,
    "PolyWorld": 36,
    "RedValley": 49,
    "River2": 23,
    "Slovenia Krvavec": 32,
    "Sportbar": 50,
    "Sports Hall": 21,
    "Subway": 15,
    "Underground Carpark": 20,
}


def setup(guilds) -> None:
    tempDict = {}

    try:
        with open(config["save_location"] + "velocidrone.json") as f:
            pass
        f.close()
    except IOError as e:
        print("Velocidrone save file not found . . . Making that shit!")
        f = open(config["save_location"] + "velocidrone.json", "w")
        f.write('{"track_priority":{"high":{},"low":[]},"guilds":{}}')
        f.close()

    with open(config["save_location"] + "velocidrone.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for guild in guilds:
        print(guild.id)
        ensure_guild_exists(guild.id)

    track_ids = get_all_tracks()

    high_priority_track_ids = config["track_priority"]["high"].keys()
    low_priority_track_ids = config["track_priority"]["low"]

    for track_id in track_ids:
        save_track(get_leaderboard(None, get_JSON_url(track_id)), track_id)
        if (
            track_id in low_priority_track_ids
            or str(track_id) in high_priority_track_ids
        ):
            continue

        config["track_priority"]["low"].append(track_id)

    save_config()


def get_leaderboard(guild_id: int, url: str) -> list:
    """Get the current leaderboard for a url

    Args:
        guild_id (int): The guilds ID
        url (str): The leaderboard as a JSON URL

    """
    velocidrone_leaderboard = []

    response = requests.get(url, timeout=100)
    if response.status_code != 200:
        raise Exception("Failed to get leaderboard, TRACK ID: ", url)

    temp_leaderboard = json.loads(response.text)

    velocidrone_leaderboard.append(temp_leaderboard[0])
    velocidrone_leaderboard.append([])

    whitelist = []

    if guild_id is not None:
        whitelist = config["guilds"][str(guild_id)]["whitelist"]
    else:
        for guild_id in config["guilds"]:
            for name in config["guilds"][str(guild_id)]["whitelist"]:
                whitelist.append(name)

    for i in temp_leaderboard[1]:
        if i["playername"] in whitelist:
            velocidrone_leaderboard[1].append(i)

    return velocidrone_leaderboard


def whitelist_add(guild_id: int, name: str) -> str:
    if name not in config["guilds"][str(guild_id)]["whitelist"]:
        config["guilds"][str(guild_id)]["whitelist"].append(name)
        save_config()
        return name
    else:
        return None


def whitelist_remove(guild_id: int, name: str) -> str:
    if name in config["guilds"][str(guild_id)]["whitelist"]:
        config["guilds"][str(guild_id)]["whitelist"].remove(name)
        save_config()
        return name
    else:
        return None


def track_add(guild_id: int, track_id: int):
    if track_id not in config["guilds"][str(guild_id)]["track_ids"]:
        try:
            config["guilds"][str(guild_id)]["track_ids"].append(track_id)
            save_config()
            url = get_JSON_url(track_id)
            save_track(
                get_leaderboard(guild_id, url),
                track_id,
            )
            add_track_to_high_priority(track_id)
            return get_track(track_id)[0]["track_name"]
        except Exception as e:
            config["guilds"][str(guild_id)]["track_ids"].remove(track_id)
            save_config()
            return None
    else:
        return get_track(track_id)[0]["track_name"]


def track_remove(guild_id: int, track_id: int):
    removed = False

    for i in config["guilds"][str(guild_id)]["track_ids"]:
        if i == track_id:
            config["guilds"][str(guild_id)]["track_ids"].remove(i)
            save_config()
            removed = True

    return get_track(track_id)[0]["track_name"] if removed else None


def save_config():
    tempDict = {}

    tempDict["track_priority"] = {}
    tempDict["guilds"] = {}

    for guild_id in config["guilds"]:
        tempDict["guilds"][str(guild_id)] = config["guilds"][str(guild_id)]

    for priority in config["track_priority"]:
        tempDict["track_priority"][priority] = config["track_priority"][priority]

    with open(config["save_location"] + "velocidrone.json", "w") as f:
        if debug:
            json.dump(
                tempDict,
                f,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )
        else:
            json.dump(tempDict, f)


def get_JSON_url(track_id: int):
    return f"https://www.velocidrone.com/leaderboard_as_json2/{0}/{6}/{track_id}/{1.16}"


def get_leaderboard_url(track_id: int):
    track_ids = get_all_tracks()

    if track_id in track_ids:
        track = get_leaderboard(None, get_JSON_url(track_id))
        scene = track[0]["scenery_name"]
        return f"https://www.velocidrone.com/leaderboard/{track_scenes[scene]}/{track_id}/All"

    return None


def save_track(json_data: list, track_id: int):
    with open(config["save_location"] + f"/track_{track_id}.json", "w") as f:
        if debug:
            json.dump(
                json_data,
                f,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )
        else:
            json.dump(json_data, f)
    f.close()


def get_whitelist():
    return config["whitelist"]


def get_track_list(guild_id: int):
    tracks = []

    tempTrack = []
    for i in config["guilds"][str(guild_id)]["track_ids"]:
        with open(config["save_location"] + f"/track_{i}.json") as f:
            tempTrack = json.load(f)
        f.close()
        tracks.append(tempTrack[0]["track_name"])

    return tracks


def get_track_and_ID_list(guild_id: int):
    tracks = []

    tempTrack = []
    for i in config["guilds"][str(guild_id)]["track_ids"]:
        with open(config["save_location"] + f"/track_{i}.json") as f:
            tempTrack = json.load(f)
        f.close()
        tracks.append((tempTrack[0]["track_name"], i))

    return tracks


def get_track(track_id: int) -> list:
    track = []

    with open(config["save_location"] + f"/track_{track_id}.json") as f:
        track = json.load(f)
    f.close()

    return track


def get_number_of_tracks(prioritized_list: bool = False):
    try:
        if prioritized_list:
            return len(generate_prioritized_track_list())
        else:
            return len(get_all_tracks())

    except Exception as e:
        return 0


async def track_update() -> dict:
    """Updates the leaderboard for all tracks and returns a dictionary of the differences between the old and new leaderboards

    Returns:
        dict: A dictionary of the differences between the old and new leaderboards
    """

    track_diff = {}
    track_ids = generate_prioritized_track_list()
    new_low_priority_track_ids = []

    for track_id in track_ids:
        if track_id in new_low_priority_track_ids:
            print(f"Skipping track {track_id} because it was deprioritized")
            continue

        await asyncio.sleep(10)

        saved_leaderboard = get_track(track_id)
        current_leaderboard = get_leaderboard(None, get_JSON_url(track_id))

        if saved_leaderboard[1] != current_leaderboard[1]:
            save_track(current_leaderboard, track_id)
            track_diff[track_id] = {}

            add_track_to_high_priority(track_id)
        else:
            if str(track_id) in config["track_priority"]["high"].keys() and (
                time.time()
                - config["track_priority"]["high"][str(track_id)]["last_changed"]
                > config["track_deprioritize_time"]
            ):
                new_low_priority_track_ids.append(track_id)
                remove_track_from_high_priority(track_id)
            continue

        for i in current_leaderboard[1]:
            first_time = True
            for j in saved_leaderboard[1]:
                if i["playername"] == j["playername"]:
                    first_time = False
                    if float(i["lap_time"]) < float(j["lap_time"]):
                        track_diff[track_id][i["playername"]] = {
                            "lap_date": i["lap_date"],
                            "lap_time": i["lap_time"],
                            "lap_diff": float(i["lap_time"]) - float(j["lap_time"]),
                            "first_time": False,
                        }
            if first_time:
                track_diff[track_id][i["playername"]] = {
                    "lap_date": i["lap_date"],
                    "lap_time": i["lap_time"],
                    "first_time": True,
                }

    return track_diff


def set_guild_leaderboard_channel(guild_id: int, channel_id: int):
    config["guilds"][str(guild_id)]["leaderboard_channel_id"] = channel_id
    save_config()


def generate_prioritized_track_list() -> list:
    """Generates a list of track IDs

    Generate a list of tracks that alternates between high priority and low priority tracks and repeats until all tracks are in the list. Duplicating high priority tracks if necessary.

    Returns:
        list: A list of track IDs prioritized by the high priority list and then the low priority list
    """

    high_priority_track_ids = list(config["track_priority"]["high"].keys())
    high_priority_track_ids = [int(i) for i in high_priority_track_ids]
    low_priority_track_ids = config["track_priority"]["low"]

    track_ids = distribute(high_priority_track_ids * 3, low_priority_track_ids)

    print(track_ids)

    return track_ids


def get_guild_track_list(guild_id: int):
    return config["guilds"][str(guild_id)]["track_ids"]


def get_guild_whitelist(guild_id: int):
    return config["guilds"][str(guild_id)]["whitelist"]


def get_guild_leaderboard_channel(guild_id: int) -> int:
    return config["guilds"][str(guild_id)]["leaderboard_channel_id"]


def get_all_tracks() -> set:
    track_ids = set()

    for guild_id in config["guilds"]:
        for track_id in config["guilds"][str(guild_id)]["track_ids"]:
            track_ids.add(track_id)

    return track_ids


def ensure_guild_exists(guild_id: int):
    if guild_id not in config["guilds"].keys():
        config["guilds"][str(guild_id)] = {
            "track_ids": [],
            "whitelist": [],
            "leaderboard_channel_id": None,
        }
        save_config()


def add_track_to_high_priority(track_id: int):
    """Adds a track to the high priority list and removes it from the low priority list

    Args:
        track_id (int): The track ID to add to the high priority list
    """
    if str(track_id) not in config["track_priority"]["high"].keys():
        config["track_priority"]["high"][str(track_id)] = {"last_changed": time.time()}

    if track_id in config["track_priority"]["low"]:
        config["track_priority"]["low"].remove(track_id)

    save_config()


def remove_track_from_high_priority(track_id: int):
    """Removes a track from the high priority list and adds it to the low priority list

    Args:
        track_id (int): The track ID to remove from the high priority list
    """
    if str(track_id) in config["track_priority"]["high"].keys():
        config["track_priority"]["high"].pop(str(track_id))

    if track_id not in config["track_priority"]["low"]:
        config["track_priority"]["low"].append(track_id)

    save_config()


def distribute(source_one, source_two) -> list:
    """Distribute the elements of source_one into source_two, returning a list.

    All elements of source_one and source_two will be included in the result, even if the lengths of the two iterables are not equal. The spacing between the elements will be equal, and the elements will be in the same order as they were in the original iterables.

    >>> list(distribute([1, 2], [5, 6, 7, 8]))
    [1, 5, 6, 2, 7, 8]
    """
    len_one, len_two = len(source_one), len(source_two)
    result = []

    if len_one == 0:
        return source_two
    if len_two == 0:
        return source_one

    ratio = (len_two + len_one - 1) // len_one

    idx_one, idx_two = 0, 0

    while idx_one < len_one or idx_two < len_two:
        if idx_one < len_one:
            result.append(source_one[idx_one])
            idx_one += 1

        for _ in range(ratio):
            if idx_two < len_two:
                result.append(source_two[idx_two])
                idx_two += 1

    return result


if __name__ == "__main__":
    # Test the function
    # url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    # https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16
    # /velocidrone_leaderboard official:False race_mode:6 track_id:888 version:1.16
    # save_track(get_leaderboard(url), 888)
    pass
