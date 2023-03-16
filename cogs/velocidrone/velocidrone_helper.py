import json
import time
import requests

# from lib.config import config as config_main

# config = config_main["velocidrone"]

debug = True

velocidrone_leaderboard = {}


def get_leaderboard(url: str) -> list:
    velocidrone_leaderboard = []

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get leaderboard")

    temp_leaderboard = json.loads(response.text)

    velocidrone_leaderboard.append(temp_leaderboard[0])
    velocidrone_leaderboard.append([])

    for i in range(min(len(temp_leaderboard[1]), 9), -1, -1):
        velocidrone_leaderboard[1].append(temp_leaderboard[1][i])

    return velocidrone_leaderboard


def save(json_data: dict):
    # TODO: Make this more efficient and only save the guild that called the function
    with open("velocidrone.json", "w") as f:
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


if __name__ == "__main__":
    # Test the function
    url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    # https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16
    # /velocidrone_leaderboard official:False race_mode:6 track_id:888 version:1.16
    save(get_leaderboard(url))
