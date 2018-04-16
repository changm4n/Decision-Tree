from collections import defaultdict
from functools import reduce

def getGiniIndex(p):
    return 1 - reduce(lambda x, y: x**2 + y**2, p)

def partition_by(inputs, attribute):

    groups = defaultdict(list)
    for input in inputs:
        key = input[0][attribute]
        groups[key].append(input)

    return groups