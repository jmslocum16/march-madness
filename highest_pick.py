import sys

high_seed_wins = 0
high_seed_losses = 0
same_seed_games = 0
for line in sys.stdin:
    line = line.strip().split("\t")
    t1seed = int(line[0])
    t1 = line[1]
    t1score = int(line[2])
    t2seed = int(line[3])
    t2 = line[4]
    t2score = int(line[5])
    if (t1score == t2score):
        raise RuntimeError()
    if (t1seed == t2seed):
        same_seed_games += 1
    elif (t1seed > t2seed and t1score > t2score):
        high_seed_wins += 1
    elif (t1seed > t2seed and t2score > t1score):
        high_seed_losses += 1
    elif (t2seed > t1seed and t2score > t1score):
        high_seed_wins += 1
    else:
        high_seed_losses += 1

print (str(high_seed_wins) + "/" + str(high_seed_wins + high_seed_losses))
print (str(same_seed_games) + " games excluded")
