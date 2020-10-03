import sys

# method to read data from file from the given command line arg into a 
# dictionary. Dictionary will have a key for each possible class connected
# to a list with all instances containing that class
def readData(dataset):
    dataFile = open(sys.argv[dataset], 'r')
    data = dict()
    # loop skips first line of file containing column headers
    for line in dataFile.readlines()[1:]:
        # if line is empty then move to next line
        if not line:
            continue
        classVal = line[-2]
        if (classVal not in data):
            data[classVal] = list()
        data[classVal].append(line)
    return data

# method to validate proper reading of data file
# !!not used in actual execution of learner, purely for file input testing
def printData(data):
    for classVal in data:
        print (classVal)
        for instance in data[classVal]:
            print(instance)
            
def attributeProbabilities(data, total0, total1):
    pAttributes = dict()
    for key in data:
        attrCount = dict()
        lineNum = 0
        for line in data[key]:
            attr = 1
            for i in range(len(data['0'][0]) - 2):
                if (i % 2) != 0:
                    continue
                if attr not in attrCount:
                    attrCount[attr] = 0
                if data[key][lineNum][i] == '1':
                    attrCount[attr] += 1 
                attr += 1
            lineNum += 1
        pAttributes[key] = dict()
        for attrs in attrCount:
            if key == '0':
                pAttributes[key][attrs] = float(attrCount[attrs]) / float(total0)
            else:
                pAttributes[key][attrs] = float(attrCount[attrs]) / float(total1)
    return pAttributes
            
def printProbabilities(pAttributes, p0, p1):
    print("P(C=c1)=", round(p0, 2), ' ', sep='', end='')
    for attr in pAttributes['0']:
        print("P(A", attr, "=0|c1)=", round((1 - pAttributes['0'][attr]), 2), ' ', sep='', end='')
        print("P(A", attr, "=1|c1)=", round((pAttributes['0'][attr]), 2), ' ', sep='', end='')
    print('')
    print("P(C=c2)=", round(p1, 2), ' ', sep='', end='')
    for attr in pAttributes['1']:
        print("P(A", attr, "=0|c2)=", round((1 - pAttributes['1'][attr]), 2), ' ', sep='', end='')
        print("P(A", attr, "=1|c2)=", round((pAttributes['1'][attr]), 2), ' ', sep='', end='')
    print('')
    
def predictClasses(pAttributes, dataTest, p0train, p1train):
    predictions = list()
    p0 = 1
    p1 = 1
    for key in dataTest:
        lineNum = 0
        for instance in dataTest[key]:
            attr = 1
            for i in range(len(dataTest[key][0]) - 2):
                if (i % 2) != 0:
                    continue
                if dataTest[key][lineNum][i] == '1':
                    p0 *= pAttributes['0'][attr]
                    p1 *= pAttributes['1'][attr]
                else:
                    p0 *= (1 - pAttributes['0'][attr])
                    p1 *= (1 - pAttributes['1'][attr])
                attr += 1
            lineNum += 1
            p0 *= p0train
            p1 *= p1train
            predictions.append('0') if p0 > p1 else predictions.append('1')
            p0 = 1
            p1 = 1
    return predictions

def getAccuracy(predictions, total0Test, totalTest):
    countCorrect = 0
    for i in range(total0Test):
        if predictions[i] == '0':
            countCorrect += 1
    for i in range(total0Test, totalTest):
        if predictions[i] == '1':
            countCorrect += 1
    print("Accuracy on test set (", totalTest, " instances): ", round(((countCorrect / totalTest) * 100), 2), "%", sep='')
    return 0


# ensure there are exactly 2 file arguments in execution
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Please execute script with exactly 1 train and 1 test file")
    sys.exit()
    
dataTrain = readData(1)
dataTest = readData(2)

total0Train = len(dataTrain['0']) # total count of training instances with class 0
total1Train = len(dataTrain['1']) # total count of training instances with class 1
totalTrain = total0Train + total1Train # total count of training instances

total0Test = len(dataTest['0'])
total1Test = len(dataTest['1'])
totalTest = total0Test + total1Test

p0train = total0Train / totalTrain
p1train = total1Train / totalTrain

pAttributes = attributeProbabilities(dataTrain, total0Train, total1Train)

printProbabilities(pAttributes, p0train, p1train)

trainPredictions = predictClasses(pAttributes, dataTrain, p0train, p1train)
testPredictions = predictClasses(pAttributes, dataTest, p0train, p1train)

getAccuracy(trainPredictions, total0Train, totalTrain)
getAccuracy(testPredictions, total0Test, totalTest)
# print(dataTrain['0'])
# printData(dataTrain)
# printData(dataTest)

