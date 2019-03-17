import sys

train_filename = sys.argv[1]
feature_subset = [int(x) for x in sys.argv[2].split(",")]

train_labels = []
train_data = []
train_results = []

first = False

train_file = open(train_filename, 'r')
for line in train_file:
    if not first:
        headers = line.strip().split("\t")
        first = True
        continue
    line = line.strip().split("\t")
    out = [line[0], line[1], line[2]]
    for i in feature_subset:
        out.append(line[i+3])
    

    print("\t".join(out))
