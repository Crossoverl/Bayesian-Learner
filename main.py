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
# --not used in actual execution of learner, purely for file input testing
def printData(data):
    for classVal in data:
        print (classVal)
        for instance in data[classVal]:
            print(instance)

# ensure there are exactly 2 file arguments in execution
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Please execute script with exactly 1 train and 1 test file")
    sys.exit()
    
dataTrain = readData(1)
dataTest = readData(2)

p0train = float()
p0train = len(dataTrain['0']) / (len(dataTrain['0']) + len(dataTrain['1']))
p1train = float() 
p1train = len(dataTrain['1']) / (len(dataTrain['0']) + len(dataTrain['1']))


print(p0train)
print(p1train)
# printData(dataTrain)
# printData(dataTest)

