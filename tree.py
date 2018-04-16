import math
import sys
from collections import Counter, defaultdict
from functools import partial
import itertools

def entropy(class_probabilites):
    return sum(-p * math.log(p, 2) for p in class_probabilites if p is not 0)

def class_probabilities(labels):
    total_count = len(labels)

    return [float(count) / float(total_count) for count in Counter(labels).values()]

def data_entropy(labeled_data):

    labels = [label[className] for _, label in labeled_data]
    probabilities = class_probabilities(labels)

    return entropy(probabilities)

def partition_entropy(subsets):
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count for subset in subsets)

def partition_by(inputs, attribute):

    groups = defaultdict(list)
    for input in inputs:
        key = input[0][attribute]
        groups[key].append(input)

    return groups

def partition_entropy_by(inputs, attribute):
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())

def build_tree(inputs, split_candidates=None):

    if split_candidates is None:
        split_candidates = allAttributes

    num_inputs = len(inputs)
    labelsCount = Counter([label[className] for _, label in inputs])

    l = list(filter(lambda x: x[1] != 0,labelsCount.items()))
    if l.count == 1:
        return l[1][0]

    c = [(x,y) for x,y in labelsCount.items()]
    ll = list(sorted(c, key=lambda x: x[1], reverse=True))
    if not split_candidates:
        result = ll[0][0]
        return result

    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))
    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates if a != best_attribute]

    # 재귀적으로 서브트리를 구축
    subtrees = { attribute_value : build_tree(subset, new_candidates) for attribute_value, subset in partitions.items()}
    subtrees[None] = ll[0][0]

    return (best_attribute, subtrees)


def classify(tree, input):

    if tree in list(classLabels):
        return tree

    attribute, subtree_dict = tree
    subtree_key = input[attribute]

    if subtree_key not in subtree_dict:
        subtree_key = None
    subtree = subtree_dict[subtree_key]

    return classify(subtree, input)




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



