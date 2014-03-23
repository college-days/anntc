resource = open("./data/t_alibaba_data.csv", "r")
print len(resource.readlines())
resource.close()

one = open("./data/one", "r")
print len(one.readlines())
one.close()

two = open("./data/two", "r")
print len(two.readlines())
two.close()

three = open("./data/three", 'r')
print len(three.readlines())
three.close()

four = open("./data/four", "r")
print len(four.readlines())
four.close()

class Sample:
    def __init__(self):
        self.user_id = -1
        self.brand_id = -1
        self.operator = -1

class BuySample():
    def __init__(self):
        self.user_id = -1
        self.brand_id = -1
        self.operator = -1

def loadData(filePath, sampleCollection, currentTraingNumber):
    sampleFile = open(filePath, "r")
    for line in sampleFile.readlines():
        lineSplit = line.split(",")
        sample = Sample()
        sample.user_id = int(lineSplit[0])
        sample.brand_id = int(lineSplit[1])
        sample.operator = int(lineSplit[2])
        sampleCollection.append(sample)

def loadBuyData(filePath, sampleCollection, currentTraingNumber):
    sampleFile = open(filePath, "r")
    for line in sampleFile.readlines():
        lineSplit = line.split(",")
        sample = Sample()
        sample.user_id = int(lineSplit[0])
        sample.brand_id = int(lineSplit[1])
        sample.operator = int(lineSplit[2])
        sampleCollection.append(sample)

def mainProcess(k):
    source = "./data/"+str(k)
    buySource = "./data/"+str(k+1)+"b"
    print buySource
    trainingSamples = []
    buySample = []

    loadData(source, trainingSamples, k)
    print len(trainingSamples)
    
    loadBuyData(buySource, buySample, k)
    print len(buySample)

if __name__ == '__main__':
    for i in xrange(3):
        mainProcess(i)
