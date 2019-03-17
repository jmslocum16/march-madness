import sys
from sklearn import datasets
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
import pickle

train_filename = sys.argv[1]
test_filename = sys.argv[2]
feature_subset = [int(x) for x in sys.argv[3].split(",")]

notest = (train_filename == test_filename)

train_labels = []
train_data = []
train_data_reduced = []
train_results = []

test_labels = []
test_data = []
test_data_reduced = []
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
    reduced_fv = []
    for i in feature_subset:
        reduced_fv.append(fv[i])
    train_data_reduced.append(reduced_fv)

classifiers = []
reduced_classifiers = []
nn_filename = "lbfgs_10-5_mlp_classifier"
nnf = open(nn_filename, 'r')
cl = pickle.loads(nnf.read())
reduced_classifiers.append(['loaded_nn', cl])

svm = svm.LinearSVC()
svm.fit(train_data, train_results)
classifiers.append(['svm', svm])

logistic = LogisticRegression(C=1.0, penalty='l1', solver='liblinear')
logistic.fit(train_data, train_results)
classifiers.append(['logistic', logistic])


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
        reduced_fv = []
        for i in feature_subset:
            reduced_fv.append(fv[i])
        test_data_reduced.append(reduced_fv)

total = len(test_data)

votes = [0] * total
for cl in classifiers:
    correct = 0
    predictions = cl[1].predict(test_data)
    
    for i in range(len(test_data)):
        my_result = predictions[i]
        votes[i] += 1 if (my_result == 1) else -1
        if (my_result == test_results[i]):
            correct += 1        
            # print (test_labels[i] + " Correct (" + str(my_result) + ")")
        else:
            print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

    print(str(cl[0]) + "\t" + str(correct) + "/" + str(total))

for cl in reduced_classifiers:
    correct = 0
    predictions = cl[1].predict(test_data_reduced)
    
    for i in range(len(test_data)):
        my_result = predictions[i]
        votes[i] += 1 if (my_result == 1) else -1
        if (my_result == test_results[i]):
            correct += 1        
            # print (test_labels[i] + " Correct (" + str(my_result) + ")")
        else:
            print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

    print(str(cl[0]) + "\t" + str(correct) + "/" + str(total))


correct = 0
for i in range(len(test_data)):
    my_result = 1 if (votes[i] > 0) else 0
    if (my_result == test_results[i]):
        correct += 1
        # print ("Voting Correct (" + str(my_result) + ")")
    else:
        print("Voting Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")


print("vote " +"\t" + str(correct) + "/" + str(total))
