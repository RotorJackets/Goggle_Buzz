import json
import time
import requests

from lib.config import config as config_main

config = config_main["velocidrone"]

debug = True


def setup() -> None:
    tempDict = {}

    try:
        with open("./cogs/velocidrone/jsons/velocidrone.json") as f:
            pass
        f.close()
    except IOError as e:
        f = open("./cogs/velocidrone/jsons/velocidrone.json", "w")
        f.write('{"whitelist": [],"track_ids": []}')
        f.close()

    with open("./cogs/velocidrone/jsons/velocidrone.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for track in config["track_ids"]:
        save_track(get_leaderboard(get_url(track[2])), track[2])


def get_leaderboard(url: str) -> list:
    velocidrone_leaderboard = []

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get leaderboard")

    temp_leaderboard = json.loads(response.text)

    velocidrone_leaderboard.append(temp_leaderboard[0])
    velocidrone_leaderboard.append([])

    for i in temp_leaderboard[1]:
        if i["playername"] in config["whitelist"]:
            velocidrone_leaderboard[1].append(i)

    return velocidrone_leaderboard


def whitelist_add(name: str) -> str:
    if name not in config["whitelist"]:
        config["whitelist"].append(name)
        save_config()
        return name
    else:
        return None


def whitelist_remove(name: str) -> str:
    if name in config["whitelist"]:
        config["whitelist"].remove(name)
        save_config()
        print(config)
        return name
    else:
        return None


def track_add(
    official: bool,
    race_mode: int,
    track_id: int,
    version: float,
) -> int:
    # TODO: Return None if ID is already in the list
    track = [official, race_mode, track_id, version]
    if track not in config["track_ids"]:
        config["track_ids"].append(track)
        save_config()
        save_track(
            get_leaderboard(get_url(track[2])),
            track[2],
        )
        return track_id
    else:
        return None


def track_remove(track_id: int) -> int:
    removed = False

    for i in config["track_ids"]:
        if i[2] == track_id:
            config["track_ids"].remove(i)
            save_config()
            removed = True

    return track_id if removed else None


def save_config():
    tempDict = {}
    tempDict["whitelist"] = config["whitelist"]
    tempDict["track_ids"] = config["track_ids"]

    with open(f"./cogs/velocidrone/jsons/velocidrone.json", "w") as f:
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


def get_url(track_id: int):
    for i in config["track_ids"]:
        if i[2] == track_id:
            return f"https://www.velocidrone.com/leaderboard_as_json2/{1 if i[0] else 0}/{i[1]}/{i[2]}/{i[3]}"

    return None


def save_track(json_data: list, track_id: int):
    with open(f"./cogs/velocidrone/jsons/track_{track_id}.json", "w") as f:
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


def get_track_list():
    tracks = []

    tempTrack = []
    for i in config["track_ids"]:
        with open(f"./cogs/velocidrone/jsons/track_{i[2]}.json") as f:
            tempTrack = json.load(f)
        f.close()
        tracks.append(tempTrack[0]["track_name"])

    return tracks


def get_track(track_id: int):
    track = []

    with open(f"./cogs/velocidrone/jsons/track_{track_id}.json") as f:
        track = json.load(f)
    f.close()

    return track


def track_update():
    track_diff = {}
    for track in config["track_ids"]:
        saved_leaderboard = get_track(track[2])
        current_leaderboard = get_leaderboard(get_url(track[2]))

        track_name = current_leaderboard[0]["track_name"]

        if saved_leaderboard[1] != current_leaderboard[1]:
            save_track(current_leaderboard, track[2])
            track_diff[track_name] = {}
        else:
            continue

        for i in current_leaderboard[1]:
            first_time = True
            for j in saved_leaderboard[1]:
                if i["playername"] == j["playername"]:
                    first_time = False
                    if i["lap_time"] < j["lap_time"]:
                        track_diff[track_name][i["playername"]] = {
                            "lap_date": i["lap_date"],
                            "lap_time": i["lap_time"],
                            "first_time": False,
                        }
            if first_time:
                track_diff[track_name][i["playername"]] = {
                    "lap_date": i["lap_date"],
                    "lap_time": i["lap_time"],
                    "first_time": True,
                }

    return track_diff


if __name__ == "__main__":
    # Test the function
    url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    # https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16
    # /velocidrone_leaderboard official:False race_mode:6 track_id:888 version:1.16
    save_track(get_leaderboard(url), 888)
