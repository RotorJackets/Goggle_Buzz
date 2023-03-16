for file_name in ["velocidrone.json", "leaderboard.json"]:
    try:
        with open(file_name) as f:
            pass
        f.close()
    except IOError as e:
        f = open(file_name, "w")
        f.write("{}")
        f.close()
