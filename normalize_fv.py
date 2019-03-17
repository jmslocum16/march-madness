import sys

f = open(sys.argv[1], 'r')

mins = None
maxes = None

fvs = []
for line in f:
    line = line.strip()
    parts = line.split("\t")
    if not mins:
        mins = [1000000.0] * (len(parts)-2)
        maxes = [-1000000.0] * (len(parts)-2)
        print(line)
    else:
        if len(parts) - 2 != len(mins):
            raise RuntimeError
        fvs.append(line)
        for i in range(0, len(parts)-2):
            v = float(parts[i+2])
            mins[i] = min(mins[i], v)
            maxes[i] = max(maxes[i], v)

for line in fvs:
    parts = line.split("\t")
    l = [parts[0], parts[1]]
    for i in range(0, len(parts)-2):
        v = (float(parts[i+2]) - mins[i]) / (maxes[i] - mins[i])
        l.append('%.3f' % v)
    print ("\t".join(l))
