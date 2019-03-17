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

predict_labels = []
predict_data = []
predict_data_reduced = []

first = False
train_file = open(train_filename, 'r')
for line in train_file:
    if not first:
        first = True
        continue
    line = line.strip().split("\t")
    result = 1 if (int(line[0]) > 0) else 0
    train_results.append(result)
    train_labels.append([line[1], line[2]])
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

first = False
test_file = open(test_filename, 'r') 
for line in test_file:
    if not first:
        first = True
        continue
    line = line.strip().split("\t")
    predict_labels.append([line[1], line[2]])
    fv = [float(x) for x in line[3:]]
    predict_data.append(fv)
    reduced_fv = []
    for i in feature_subset:
        reduced_fv.append(fv[i])
    predict_data_reduced.append(reduced_fv)

total = len(predict_data)

votes = [0] * total
for cl in classifiers:
    predictions = cl[1].predict(predict_data)
    print(str(cl[0]))
    
    for i in range(len(predict_data)):
        my_result = predictions[i]
        votes[i] += 1 if (my_result == 1) else -1
        print predict_labels[i][1-my_result]



for cl in reduced_classifiers:
    predictions = cl[1].predict(predict_data_reduced)
    print(str(cl[0]))
    
    for i in range(len(predict_data)):
        my_result = predictions[i]
        votes[i] += 1 if (my_result == 1) else -1
        print predict_labels[i][1-my_result]

correct = 0
print("Voting")
for i in range(len(predict_data)):
    my_result = 1 if (votes[i] > 0) else 0
    print predict_labels[i][1-my_result]

