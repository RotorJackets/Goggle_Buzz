import json
import time
from lib.config import config

# Opening JSON file
with open("leaderboard.json") as f:
    leaderboard = json.load(f)

for user in leaderboard:
    print(type(user))

f.close()


def author_check(user_ID: int):
    user_ID = str(user_ID)

    if leaderboard.get(user_ID) is None:
        print(f"Author not found, adding {user_ID} to leaderboard.")
        leaderboard[user_ID] = {"level": 1, "xp": 0, "last_message": time.time()}


def adjust_xp(user_ID: int, xp: int):
    user_ID = str(user_ID)
    level_up = False

    author_check(user_ID)
    if time.time() - leaderboard[user_ID]["last_message"] > config["delay_XP_seconds"]:
        leaderboard[user_ID]["xp"] += xp
        if leaderboard[user_ID]["xp"] >= config["level_up_XP"]:
            leaderboard[user_ID]["level"] += 1
            leaderboard[user_ID]["xp"] = 0
            level_up = True
        leaderboard[user_ID]["last_message"] = time.time()

    if level_up:
        return leaderboard[user_ID]["level"]
    else:
        return None


def get_leaders():
    sorted_leaderboard = sorted(
        leaderboard,
        key=lambda x: (leaderboard[x]["level"], leaderboard[x]["xp"]),
        reverse=True,
    )

    if (length := len(sorted_leaderboard)) < 10:
        for i in range(length - 1, 10):
            sorted_leaderboard.append(sorted_leaderboard[length - 1])

    sorted_leaders = [None] * 10
    for i in range(10):
        sorted_leaders[i] = [sorted_leaderboard[i], leaderboard[sorted_leaderboard[i]]]

    return sorted_leaders


def save():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)
    f.close()
