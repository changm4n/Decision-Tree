from collections import Counter, defaultdict
from functools import reduce
import math

def getExpectedInformation(D, attr):
    partitions = makePartitions(D, attr)
    return partition_entropy(partitions.values())

def makePartitions(D, attr):
    partitions = defaultdict(list)
    for data in D:
        category = data[0][attr]
        partitions[category].append(data)
    return partitions

def calcSumOfI(subsets):
    total = len([data for subset in subsets for data in subset])
    return sum(len(subset) / total * data_entropy(subset) for subset in subsets)

def data_entropy(labeled_data):
    labels = [list(label.items())[0][1] for _, label in labeled_data]
    ps = [float(count) / float(len(labels)) for count in Counter(labels).values()]

    return sum(-p * math.log(p, 2) for p in ps if p != 0)

def calcGiniIndex(ps):
    return 1 - reduce(lambda x, y: x**2 + y**2, ps)






