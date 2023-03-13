try:
    with open("leaderboard.json") as f:
        pass
    f.close()
except IOError as e:
    f = open("leaderboard.json", "w")
    f.write("{}")
    f.close()
