import sys
fname = sys.argv[1]
slashIndex = fname.rfind("/")
prefixIndex = fname.index("-")
prefix = fname[slashIndex+1:prefixIndex]
f = open(fname, 'r')
for line in f:
    line = line.strip()
    print(prefix + " " + line)
