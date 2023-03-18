config = {
    "command_prefix": "!",
    "guilds": [473695678690885632, 723199784697200810],
    "cogs": [
        "cogs.leaderboard.leaderboard",
        "cogs.moderator.moderator",
        "cogs.fun.fun",
        "cogs.velocidrone.velocidrone",
    ],
    "leaderboard": {
        "level_up_XP": 800,
        "random_xp_range": [15, 50],
        "delay_XP_seconds": 30,
        "leaderboard_save_interval_seconds": 25,
        "leaderboard_delete_after_seconds": 120,
    },
    "velocidrone": {
        "leaderboard_delete_after_seconds": 60,
        "track_update_interval": 10,
        "leaderboard_channel_id": 1086650100035629096,
        "velocidrone_edit_role": "Moderator",
    },
}
