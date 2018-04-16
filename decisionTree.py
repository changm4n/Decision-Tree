import math
import sys
from collections import Counter, defaultdict
import itertools
from utils import *



def build_tree(D, split_candidates=None):

    if split_candidates is None:
        split_candidates = allAttributes

    num_inputs = len(D)
    labelsCount = Counter([label[className] for _, label in D])

    l = list(filter(lambda x: x[1] != 0,labelsCount.items()))
    if l.count == 1:
        return l[1][0]

    c = [(x,y) for x,y in labelsCount.items()]
    ll = list(sorted(c, key=lambda x: x[1], reverse=True))
    if not split_candidates:
        result = ll[0][0]
        return result

    information_gains = {}
    for candidate in split_candidates:
        information_gains[candidate] = getExpectedInformation(D,candidate)

    best_attribute = min(information_gains, key = information_gains.get)
    partitions = partition_by(D, best_attribute)

    new_candidates = list(filter(lambda x: x != best_attribute, split_candidates))

    subtrees = { attribute_value : build_tree(subset, new_candidates) for attribute_value, subset in partitions.items()}
    subtrees[None] = ll[0][0]

    return (best_attribute, subtrees)

def classify(tree, d):

    if tree in list(classLabels):
        return tree

    attribute, subtree_dict = tree
    subtree_key = d[attribute]

    if subtree_key not in subtree_dict:
        subtree_key = None
    subtree = subtree_dict[subtree_key]

    return classify(subtree, d)



train_file = open(sys.argv[1], 'r')
test_file = open(sys.argv[2], 'r')
result_file = open(sys.argv[3], 'w')

trainData = train_file.read().split('\n')

allAttributes = trainData[0].split('\t')[:-1]
className = trainData[0].split('\t')[-1]
classLabels = set()

trainInput = []
for line in trainData[1:-1]:
    dic = {}
    for val, key in zip(line.split('\t'), allAttributes):
        dic[key] = val
    classLabel = line.split('\t')[-1]
    trainInput.append((dic,{className : classLabel}))

    classLabels.add(classLabel)

DTree = build_tree(trainInput)

testData = test_file.read().split('\n')

testInput = []
for line in testData[1:-1]:
    dic = {}
    for val, key in zip(line.split('\t'), allAttributes):
        dic[key] = val
    testInput.append(dic)


resultData = []
for test in testInput:
    result = classify(DTree,test)
    resultData.append((test,result))

resultString = "\t".join(allAttributes) + "\t" + className + "\n"
for data in resultData:
    resultString += "\t".join(data[0].values()) + "\t" + data[1] + "\n"

result_file.write(resultString)



