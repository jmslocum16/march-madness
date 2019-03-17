import sys
from sklearn import datasets
from sklearn.naive_bayes import GaussianNB

train_filename = sys.argv[1]
test_filename = sys.argv[2]

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

gnb = GaussianNB()
gnb.fit(train_data, train_results)

if (notest):
    test_labels = train_labels
    test_data = train_data
    test_results = train_results
else:
    first = False
    test_file = open(test_filename, 'r') 
    for line in test_file:
        if not first:
            first = True
            continue
        line = line.strip().split("\t")
        result = 1 if (int(line[0]) > 0) else 0
        test_results.append(result)
        test_labels.append(line[1] + " vs " + line[2])
        fv = [float(x) for x in line[3:]]
        test_data.append(fv)

total = len(test_data)
correct = 0

predictions = gnb.predict(test_data)

for i in range(len(test_data)):
    my_result = predictions[i]
    if (my_result == test_results[i]):
        correct += 1        
        print (test_labels[i] + " Correct (" + str(my_result) + ")")
    else:
        print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

print(str(correct) + "/" + str(total))
