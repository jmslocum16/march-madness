import sys

data_file = sys.argv[1]
results_file = sys.argv[2]


data_by_team = {}

df = open(data_file, 'r')
dr = open(results_file, 'r')

mins = None
maxes = None
first_line = None
for line in df:
    line = line.strip()
    if not first_line:
        first_line = line.split("\t")
        size = len(line.split("\t")) - 2
        mins = [1000000.0] * size
        maxes = [-1000000.0] * size
    else:
        parts = line.split("\t")
        data_by_team[parts[0]] = parts

all_games = []

# normalize

for line in dr:
    line = line.strip()
    parts = line.split("\t")
    t1name = parts[1]
    t2name = parts[4]
    t1 = data_by_team[t1name]
    t2 = data_by_team[t2name]
    t1score = int(parts[2])
    t2score = int(parts[5])
    score_diff = t1score - t2score

    game = [str(score_diff), t1name, t2name]
    game2 = [str(-score_diff), t2name, t1name]
    for i in range(len(mins)):
        v = float(t1[i+2]) - float(t2[i+2])
        mins[i] = min(mins[i], v)
        mins[i] = min(mins[i], -v)
        maxes[i] = max(maxes[i], v)
        maxes[i] = max(maxes[i], -v)
        game.append(str(v))
        game2.append(str(-v))
    all_games.append(game)
    all_games.append(game2)

headers = ["Score Diff", "Team 1", "Team 2"] + first_line[2:]
print("\t".join(headers))
for game in all_games:
    out = [game[0], game[1], game[2]]
    for i in range(len(game) - 3):
        v = (float(game[i+3]) - mins[i]) / (maxes[i] - mins[i])
        out.append( '%.3f' % v)
    print "\t".join(out)
