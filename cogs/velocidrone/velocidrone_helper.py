import json
import time
import requests


def get_leaderboard(url: str) -> dict:
    """Gets the leaderboard from the given URL"""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get leaderboard")
    return json.loads(response.text)

if __name__ == "__main__":
    # Test the function
    url = "https://www.velocidrone.com/leaderboard_as_json2/0/6/888/1.16"
    print(get_leaderboard(url))