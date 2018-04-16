import math
import sys
from collections import Counter, defaultdict
import itertools
from utils import *

def makeTree(D, attrs):

    num_inputs = len(D)
    labelsCount = Counter([label[className] for _, label in D])

    l = list(filter(lambda x: x[1] != 0,labelsCount.items()))
    if l.count == 1:
        return l[1][0]

    c = [(x,y) for x,y in labelsCount.items()]
    ll = list(sorted(c, key=lambda x: x[1], reverse=True))

    if not attrs:
        result = ll[0][0]
        return result

    information_gains = {}
    for attr in attrs:
        information_gains[attr] = getExpectedInformation(D,attr)

    nextAttr = min(information_gains, key = information_gains.get)
    partitions = makePartitions(D, nextAttr)

    remainAttrs = list(filter(lambda x: x != nextAttr, attrs))

    subtrees = { attr : makeTree(subset, remainAttrs) for attr, subset in partitions.items()}
    subtrees['EOT'] = ll[0][0]

    return (nextAttr, subtrees)

def classify(tree, d):

    if tree in list(classLabels):
        return tree

    attr, subDict = tree
    subtree_key = d[attr]

    if subtree_key not in subDict:
        subtree_key = 'EOT'

    subtree = subDict[subtree_key]

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

DTree = makeTree(trainInput, allAttributes)

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



