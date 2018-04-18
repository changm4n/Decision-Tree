import math
import sys
from collections import Counter, defaultdict
import itertools
from utils import *

def makeTree(D, attrs, pVote = None):

    num_inputs = len(D)
    labelsCount = list(filter(lambda x: x[1] != 0,Counter([l[className] for _, l in D]).items()))

    #한 클래스만 존재한다면 return
    if labelsCount.count == 1:
        return labelsCount[1][0]

    #클래스들의 빈도를 내림차순으로 저장.
    #빈도수가 가장 높은값이 중복 존재한다면, 인자로 받은 부모 노드에서의 결과 반영
    ll = list(sorted(labelsCount, key=lambda x: x[1], reverse=True))
    maxList = list(filter(lambda x: x[1] == ll[0][1], ll))
    voteResult = ll[0][0]

    if len(maxList) != 1 and pVote in [x[0] for x in maxList]:
        voteResult = pVote

    #더이상 파티션할 Attribute가 없다면, 다수결로 결과를 return
    if not attrs:
        return voteResult

    #파티션 가능한 Attribute들을 기준으로 Information Gain값 계산.
    information_gains = {}
    for attr in attrs:
        information_gains[attr] = getExpectedInformation(D,attr)

    #Info(D)의 값은 모두 동일하므로, InfoA(D)값들의 최소값을 기준으로
    #다음 파티션할 Attribute 선정.
    nextAttr = min(information_gains, key = information_gains.get)
    partitions = makePartitions(D, nextAttr)

    #선정된 Attribute를 제외하고, 다음 재귀시점으로 넘김
    remainAttrs = list(filter(lambda x: x != nextAttr, attrs))

    nextTree = { attr : makeTree(subset, remainAttrs, ll[0][0]) for attr, subset in partitions.items()}
    # Train되지 않은 label에 대해선 다수결 결과값 return
    nextTree['EOT'] = voteResult

    return {"nextAttr":nextAttr,
            "subTree":nextTree}

def classify(tree, d):

    #클래스값이 정의되었다면, 결과 return
    if tree in list(classLabels):
        return tree

    #다음으로 구분할 Attribute를 이용하여
    #Data의 Label을 조회, subTree 생성
    nextAttr = d[tree["nextAttr"]]

    # 만약 해당 Label에 대한 트리가 만들어지지 않았다면
    # 다수결 값 return하도록 설정.
    if nextAttr not in tree["subTree"]:
        nextAttr = 'EOT'

    #해당 Attribute로 subTree 접근
    subtree = tree["subTree"][nextAttr]

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



