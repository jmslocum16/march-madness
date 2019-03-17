import sys
fname = sys.argv[1]
slashIndex = fname.rfind("/")
prefixIndex = fname.index("-")
prefix = fname[slashIndex+1:prefixIndex]
prefix = prefix[2:]
f = open(fname, 'r')
for line in f:
    line = line.strip()
    parts = line.split("\t")
    parts = list(filter(None, parts))
    parts[1] = prefix + " " + parts[1]
    parts[4] = prefix + " " + parts[4]
    print "\t".join(parts)
