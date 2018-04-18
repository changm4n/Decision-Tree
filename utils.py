from collections import Counter, defaultdict
from functools import reduce
import math

def getExpectedInformation(D, attr):
    partitions = makePartitions(D, attr)
    return calcI(partitions.values())

def makePartitions(D, attr):
    #defaultdict을 활용하여 label에 따라 파티션을 생성합니다.
    partitions = defaultdict(list)
    for data in D:
        category = data[0][attr]
        partitions[category].append(data)
    return partitions

def calcI(subsets):
    #계산된 확률들을 기반하여 InfoA(D)값을 계산합니다.
    total = len([d for s in subsets for d in s])
    return sum(len(s) / total * calcSumOfP(s) for s in subsets)

def calcSumOfP(D):
    #Label들의 List를 활용하여 Label별 -p * log2(p)의 합을 계산합니다.
    labels = [list(label.items())[0][1] for _, label in D]
    ps = [float(count) / float(len(labels)) for count in Counter(labels).values()]

    return sum(-p * math.log(p, 2) for p in ps if p != 0)

def calcGiniIndex(ps):
    return 1 - reduce(lambda x, y: x**2 + y**2, ps)
