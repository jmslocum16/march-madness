from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
import sys

train_filename = sys.argv[1]

train_labels = []
train_data = []
train_results = []

first = False

train_file = open(train_filename, 'r')
for line in train_file:
    if not first:
        headers = line.strip().split("\t")
        first = True
        continue
    line = line.strip().split("\t")
    result = 1 if (int(line[0]) > 0) else 0
    train_results.append(result)
    fv = [float(x) for x in line[3:]]
    train_data.append(fv)
    train_labels.append(line[0:3])

print (len(train_data), len(train_data[0]))

logistic = LogisticRegression(C=1.0, penalty='l1', solver='liblinear')
logistic.fit(train_data, train_results)
model = SelectFromModel(logistic, prefit=True)

new_train_data = model.transform(train_data)

support = model.get_support()

#headers_used = [headers[0], headers[1], headers[2]]
#for i, use in enumerate(support):
#    if use:
#        headers_used.append(headers[i+3])
#print "\t".join(headers_used)
#for i, d in enumerate(new_train_data.tolist()):
#    fvout = ['%.3f' % x for x in d]
#    l = train_labels[i] + fvout
#    print "\t".join(l)

indexes = []
for i, use in enumerate(support):
    if use:
        indexes.append(i)

print(",".join(str(i) for i in indexes))
