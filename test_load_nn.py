import sys
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
import pickle

train_filename = sys.argv[1]
test_filename = sys.argv[2]
do_regression = (int(sys.argv[3]) != 0)

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
    result_reg = float(line[0])
    result_class = 1 if (result_reg > 0) else 0
    train_results.append(result_reg if do_regression else result_class)
    train_labels.append(line[1] + " vs " + line[2])
    fv = [float(x) for x in line[3:]]
    train_data.append(fv)

classifiers = []

if do_regression:
    nn_filename = "lbfgs_20-5-2_mlp_regression"
else:
    nn_filename = "lbfgs_10-5_mlp_classifier"
nnf = open(nn_filename, 'r')
cl = pickle.loads(nnf.read())   
classifiers.append(['loaded', cl])

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
        result_reg = int(line[0])
        result_class = 1 if (result_reg > 0) else 0
        test_results.append(result_reg if do_regression else result_class)
        test_labels.append(line[1] + " vs " + line[2])
        fv = [float(x) for x in line[3:]]
        test_data.append(fv)

total = len(test_data)

for cl in classifiers:
    correct = 0
    predictions = cl[1].predict(test_data)
    
    for i in range(len(test_data)):
        if do_regression:
            my_result = 1 if (predictions[i] > 0) else 0
            their_result = 1 if (test_results[i] > 0) else 0
        else:
            my_result = predictions[i]
            their_result = test_results[i]
        if (my_result == their_result):
            correct += 1        
            # print (test_labels[i] + " Correct (" + str(my_result) + ")")
        # else:
        #    print(test_labels[i] + " Incorrect. Predicted (" + str(my_result) + "), actual (" + str(test_results[i]) + ")")

    print(str(cl[0]) + "\t" + str(correct) + "/" + str(total))
    if (correct >= 180):
        save_fname = str(cl[0])
        print("Saving " + str(cl[0]))
        s = pickle.dumps(cl[1])
        sf = open(save_fname, 'w')
        sf.write(s)
        sf.close()
