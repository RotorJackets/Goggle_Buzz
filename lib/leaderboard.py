import json
import time
from lib.config import config

# Opening JSON file
with open("leaderboard.json") as f:
    leaderboard = json.load(f)

f.close()


def author_check(guild_ID: int, user_ID: int):
    user_ID = str(user_ID)
    guild_ID = str(guild_ID)

    if leaderboard.get(guild_ID) is None:
        print(f"Guild not found, adding {guild_ID} to leaderboard.")
        leaderboard[guild_ID] = {}

    if leaderboard[guild_ID].get(user_ID) is None:
        print(f"Author not found, adding {user_ID} to leaderboard.")
        leaderboard[guild_ID][user_ID] = {
            "level": 1,
            "xp": 0,
            "place": 0,
            "last_message": time.time(),
        }


def adjust_xp(guild_ID: int, user_ID: int, xp: int):
    user_ID = str(user_ID)
    guild_ID = str(guild_ID)
    level_up = False

    author_check(guild_ID, user_ID)
    if (
        time.time() - leaderboard[guild_ID][user_ID]["last_message"]
        > config["delay_XP_seconds"]
    ):
        leaderboard[guild_ID][user_ID]["xp"] += xp
        if leaderboard[guild_ID][user_ID]["xp"] >= config["level_up_XP"]:
            leaderboard[guild_ID][user_ID]["level"] += 1
            leaderboard[guild_ID][user_ID]["xp"] = 0
            level_up = True
        leaderboard[guild_ID][user_ID]["last_message"] = time.time()

    if level_up:
        return leaderboard[guild_ID][user_ID]["level"]
    else:
        return None


def get_leaders(guild_ID: int):
    guild_ID = str(guild_ID)

    sorted_leaderboard = sorted(
        leaderboard[guild_ID],
        key=lambda x: (
            leaderboard[guild_ID][x]["level"],
            leaderboard[guild_ID][x]["xp"],
        ),
        reverse=True,
    )

    for i in range(len(sorted_leaderboard)):
        leaderboard[guild_ID][sorted_leaderboard[i]]["place"] = i + 1
    
    save()

    sorted_leaders = []
    for i in range(len(sorted_leaderboard) if len(sorted_leaderboard) < 11 else 10):
        sorted_leaders.append(
            [sorted_leaderboard[i], leaderboard[guild_ID][sorted_leaderboard[i]]]
        )

    return sorted_leaders

def get_info(guild_ID: int, user_ID: int):
    user_ID = str(user_ID)
    guild_ID = str(guild_ID)

    author_check(guild_ID, user_ID)
    return leaderboard[guild_ID][user_ID]

def save():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)
    f.close()
