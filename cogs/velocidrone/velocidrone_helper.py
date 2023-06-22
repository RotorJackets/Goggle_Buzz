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


def setup() -> None:
    tempDict = {}

    try:
        with open(config["save_location"] + "velocidrone.json") as f:
            pass
        f.close()
    except IOError as e:
        print("Velocidrone save file not found . . . Making that shit!")
        f = open(config["save_location"] + "velocidrone.json", "w")
        f.write('{"whitelist": [],"track_ids": []}')
        f.close()

    with open(config["save_location"] + "velocidrone.json") as f:
        tempDict = json.load(f)

    f.close()

    for key in tempDict.keys():
        config[key] = tempDict[key]

    for track_id in config["track_ids"]:
        save_track(get_leaderboard(get_JSON_url(track_id)), track_id)


def get_leaderboard(url: str) -> list:
    velocidrone_leaderboard = []

    response = requests.get(url, timeout=100)
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
        return name
    else:
        return None


def track_add(
    track_id: int,
) -> str:
    if track_id not in config["track_ids"]:
        try:
            config["track_ids"].append(track_id)
            save_config()
            url = get_JSON_url(track_id)
            save_track(
                get_leaderboard(url),
                track_id,
            )
            return get_track(track_id)[0]["track_name"]
        except Exception as e:
            config["track_ids"].remove(track_id)
            save_config()
            return None
    else:
        return get_track(track_id)[0]["track_name"]


def track_remove(track_id: int) -> str:
    removed = False

    for i in config["track_ids"]:
        if i == track_id:
            config["track_ids"].remove(i)
            save_config()
            removed = True

    return get_track(track_id)[0]["track_name"] if removed else None


def save_config():
    tempDict = {}
    tempDict["whitelist"] = config["whitelist"]
    tempDict["track_ids"] = config["track_ids"]

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
    if track_id in config["track_ids"]:
        return f"https://www.velocidrone.com/leaderboard_as_json2/{0}/{6}/{track_id}/{1.16}"

    return None


def get_leaderboard_url(track_id: int):
    if track_id in config["track_ids"]:
        track = get_leaderboard(get_JSON_url(track_id))
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


def get_track_list():
    tracks = []

    tempTrack = []
    for i in config["track_ids"]:
        with open(config["save_location"] + f"/track_{i}.json") as f:
            tempTrack = json.load(f)
        f.close()
        tracks.append(tempTrack[0]["track_name"])

    return tracks


def get_track(track_id: int) -> list:
    track = []

    with open(config["save_location"] + f"/track_{track_id}.json") as f:
        track = json.load(f)
    f.close()

    return track


def track_update():
    track_diff = {}
    for track_id in config["track_ids"]:
        saved_leaderboard = get_track(track_id)
        current_leaderboard = get_leaderboard(get_JSON_url(track_id))

        if saved_leaderboard[1] != current_leaderboard[1]:
            save_track(current_leaderboard, track_id)
            track_diff[track_id] = {}
        else:
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


if __name__ == "__main__":
    # Test the function
    # url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    # https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16
    # /velocidrone_leaderboard official:False race_mode:6 track_id:888 version:1.16
    # save_track(get_leaderboard(url), 888)
    pass
