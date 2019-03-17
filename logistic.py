import sys
from sklearn import datasets
from sklearn.linear_model import LogisticRegression

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

classifiers = []
for c in [1.0, 0.1, 0.01]:
#    classifiers.append(['lifgs ovr '+ str(c), LogisticRegression(C=c, penalty='l2', solver='lbfgs')])
#    classifiers.append(['lifgs multi '+ str(c), LogisticRegression(C=c, penalty='l2', solver='lbfgs', multi_class='multinomial')])
#    classifiers.append(['saga l2 '+ str(c), LogisticRegression(C=c, penalty='l2', solver='saga', multi_class='multinomial')])
#    classifiers.append(['saga l1 '+ str(c), LogisticRegression(C=c, penalty='l1', solver='saga', multi_class='multinomial')])
    classifiers.append(['liblinear l2 '+ str(c), LogisticRegression(C=c, penalty='l2', solver='liblinear')])
    classifiers.append(['liblinear l1 '+ str(c), LogisticRegression(C=c, penalty='l1', solver='liblinear')])

for cl in classifiers:
    cl[1].fit(train_data, train_results)
 

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

for cl in classifiers:
    correct = 0
    predictions = cl[1].predict(test_data)
    
    for i in range(len(test_data)):
        my_result = predictions[i]
        if (my_result == test_results[i]):
            correct += 1        
            # print (test_labels[i] + " Correct (" + str(my_result) + ")")
        # else:
        #    print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

    print(str(cl[0]) + "\t" + str(correct) + "/" + str(total))
