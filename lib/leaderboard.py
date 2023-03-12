import json
import time

# Opening JSON file
with open("leaderboard.json") as f:
    leaderboard = json.load(f)

for user in leaderboard:
    print(type(user))

f.close()

delay_XP_seconds = 0
level_up_XP = 10


def author_check(user_ID: int):
    user_ID = str(user_ID)

    if leaderboard.get(user_ID) is None:
        print(f"Author not found, adding {user_ID} to leaderboard.")
        leaderboard[user_ID] = {"level": 1, "xp": 0, "last_message": time.time()}
        with open("leaderboard.json", "w") as f:
            json.dump(leaderboard, f)
        f.close()


def adjust_xp(user_ID: int, xp: int):
    user_ID = str(user_ID)
    level_up = False

    author_check(user_ID)
    if time.time() - leaderboard[user_ID]["last_message"] > delay_XP_seconds:
        leaderboard[user_ID]["xp"] += xp
        if leaderboard[user_ID]["xp"] >= level_up_XP:
            leaderboard[user_ID]["level"] += 1
            leaderboard[user_ID]["xp"] = 0
            level_up = True
        leaderboard[user_ID]["last_message"] = time.time()

    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)
    f.close()

    if level_up:
        return leaderboard[user_ID]["level"]
    else:
        return None
