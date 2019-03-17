import sys

train_filename = sys.argv[1]
test_filename = sys.argv[2]
k = int(sys.argv[3])
exp = int(sys.argv[4])

notest = (train_filename == test_filename)

train_labels = []
train_data = []
train_results = []

test_labels = []
test_data = []
test_results = []

first = False
train_file = open(train_filename, 'r')
for line in train_file:
    if not first:
        first = True
        continue
    line = line.strip().split("\t")
    result = 1 if (int(line[0]) > 0) else 0
    train_results.append(result)
    train_labels.append(line[1] + " vs " + line[2])
    fv = [float(x) for x in line[3:]]
    train_data.append(fv)

if (notest):
    test_labels = train_labels
    test_data = train_data
    test_results = train_results
else:
    first = False
    test_file = open(test_filename, 'r') 
    for line in train_file:
        if not first:
            first = true
            continue
        line = line.strip().split("\t")
        result = 1 if (int(line[0]) > 0) else 0
        test_results.append(result)
        test_labels.append(line[1] + " vs " + line[2])
        fv = [float(x) for x in line[3:]]
        test_data.append(fv)

total = len(test_data)
correct = 0

for i in range(len(test_data)):
    my_fv = test_data[i]
    # print("test " + test_labels[i] + "\t:\t" + "\t".join(['%.3f' % x for x in my_fv]) + "\t(" + str(test_results[i]) + ")")
    dist_and_results = []
    for j in range(len(train_data)):
        if (i==j and notest):
            continue
        their_fv = train_data[j]
        # print("\t\t " + train_labels[j] + "\t:\t" + "\t".join(['%.3f' % x for x in their_fv]) + "\t(" + str(train_results[j]) + ")")
        dist = 0.0
        for x in range(len(my_fv)):
            feature_dist = abs(my_fv[x] - their_fv[x])
            if (exp != 1):
                feature_dist = feature_dist ** exp
            dist += feature_dist

        dist_and_results.append((dist, j, train_results[j]))

    dist_and_results.sort()
    count1 = 0.0
    count0 = 0.0
    limit = min(len(dist_and_results), k)
    for x in range(limit):
        dr = dist_and_results[x]
        xxx = (limit - x) / (1.0*limit)
        if (dr[2] == 1):
            count1 += xxx
        elif (dr[2] == 0):
            count0 += xxx
    my_result = 1 if count1 > count0 else 0
    if (my_result == test_results[i]):
        correct += 1        
        print (test_labels[i] + " Correct (" + str(my_result) + ")")
    else:
        print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

print(str(correct) + "/" + str(total))
