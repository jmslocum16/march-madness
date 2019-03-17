import sys
import random

file = sys.argv[1]
test_pct = int(sys.argv[2])

f = open(file, 'r')
train_f = open("train-"+file, 'w')
test_f = open("test-"+file, 'w')

for line in f:
    x = random.randint(0, 99)
    if x < test_pct:
        test_f.write(line)
    else:
        train_f.write(line)

train_f.close()
test_f.close()
