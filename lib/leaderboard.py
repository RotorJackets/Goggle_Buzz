import json
import time
import random
import discord
from lib.config import config

# Opening JSON file
with open("leaderboard.json") as f:
    leaderboard = json.load(f)

debug = True

f.close()


def author_check(guild: discord.guild.Guild, member: discord.member.Member):
    member_ID = str(member.id)
    guild_ID = str(guild.id)

    if leaderboard.get(guild_ID) is None:
        print(f"Guild not found, adding {guild_ID} to leaderboard.")
        leaderboard[guild_ID] = {}

    if leaderboard[guild_ID].get(member_ID) is None:
        print(f"Author not found, adding {member_ID} to leaderboard.")
        leaderboard[guild_ID][member_ID] = {
            "level": 1,
            "xp": 0,
            "place": 0,
            "last_message": time.time(),
        }


def adjust_xp(
    guild: discord.guild.Guild,
    member: discord.member.Member,
    xp: int = random.randint(
        config["random_xp_range"][0], config["random_xp_range"][1]
    ),
):
    member_ID = str(member.id)
    guild_ID = str(guild.id)
    level_up = False

    author_check(guild, member)
    if (
        time.time() - leaderboard[guild_ID][member_ID]["last_message"]
        > config["delay_XP_seconds"]
    ):
        leaderboard[guild_ID][member_ID]["xp"] += xp
        if leaderboard[guild_ID][member_ID]["xp"] >= config["level_up_XP"]:
            leaderboard[guild_ID][member_ID]["level"] += 1
            leaderboard[guild_ID][member_ID]["xp"] = 0
            level_up = True
        leaderboard[guild_ID][member_ID]["last_message"] = time.time()

    if level_up:
        return leaderboard[guild_ID][member_ID]["level"]
    else:
        return None


def get_leaders(guild: discord.guild.Guild):
    guild_ID = str(guild.id)

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

    save(guild)

    sorted_leaders = []
    for i in range(len(sorted_leaderboard) if len(sorted_leaderboard) < 11 else 10):
        sorted_leaders.append(
            [sorted_leaderboard[i], leaderboard[guild_ID][sorted_leaderboard[i]]]
        )

    return sorted_leaders


def get_info(guild: discord.guild.Guild, member: discord.member.Member):
    member_ID = str(member.id)
    guild_ID = str(guild.id)

    author_check(guild, member)
    get_leaders(guild)
    return leaderboard[guild_ID][member_ID]


def save(guild: discord.guild.Guild):
    # TODO: Make this more efficient and only save the guild that called the function
    with open("leaderboard.json", "w") as f:
        if debug:
            json.dump(
                leaderboard,
                f,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )
        else:
            json.dump(leaderboard, f)
    f.close()


def reset_guild(guild: discord.guild.Guild):
    guild_ID = str(guild.id)

    if leaderboard.get(guild_ID) is None:
        leaderboard[guild_ID] = {}

    with open("leaderboard.json.backup", "a") as f:
        f.writelines(["\n"])
        f.writelines(["\n", f"{time.time()} | {guild_ID} \n"])
        json.dump(leaderboard[guild_ID], f)
    f.close()

    leaderboard[guild_ID] = {}
    save(None)
