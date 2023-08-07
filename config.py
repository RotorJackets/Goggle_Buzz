config = {
    "command_prefix": "!",
    "cogs": [
        "cogs.leaderboard.leaderboard",
        "cogs.fun.fun",
        "cogs.velocidrone.velocidrone",
        "cogs.util.join_message",
    ],
    "leaderboard": {
        "whitelisted_guilds": [723199784697200810],
        "level_up_XP": 800,
        "random_xp_range": [15, 50],
        "delay_XP_seconds": 0,
        "leaderboard_save_interval_seconds": 25,
        "leaderboard_delete_after_seconds": 120,
        "save_location": "cogs/leaderboard/json/",
    },
    "velocidrone": {
        "track_update_interval": 200,
        "track_deprioritize_time": 86400,
        "velocidrone_edit_role": "Researcher",
        "save_location": "cogs/velocidrone/json/",
    },
    "util": {
        "welcome_channel": 1086687733315022918,
        "new_member_info_channel": 1074547682112192562,
        "build_help_channel": 1082508044048552056,
        "introductions_channel": 1086061074215878737,
        "shipping_channel": "shipping-sharing",
        "order_role": "RotorJacket",
    },
}
