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

    save_track(get_leaderboard("https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"), 888)


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


def save_config():
    tempDict = {}
    tempDict["whitelist"] = config["whitelist"]
    tempDict["track_ids"] = config["track_ids"]

    print(tempDict)

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


def track_diff(track_id: int):
    try:
        with open(f"./cogs/velocidrone/jsons/track_{track_id}.json") as f:
            pass
        f.close()
        return True
    except IOError as e:
        return False


if __name__ == "__main__":
    # Test the function
    url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    # https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16
    # /velocidrone_leaderboard official:False race_mode:6 track_id:888 version:1.16
    save_track(get_leaderboard(url), 888)
