import os
from calcUtil import initList
from calcUtil import getNetOutput
from calcUtil import updateHiddenWeight
from calcUtil import updateOutputWeight
import time

INPUTNODENUMBER = 4
HIDDENNODENUMBER = 2
ANNSTEP = 0.001
ANNPRECISION = 0.000001
MAXTIME = 33333

class HiddenNode():
    def __init__(self):
        self.input = []
        self.weight = initList(INPUTNODENUMBER)

    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

    def updateWeightNew(self, delta, weight):
        self.weight = updateHiddenWeight(self.input, self.weight, self.getOutputNew(), ANNSTEP, delta, weight)

    def updateInput(self, input):
        self.input = [1.0] + input

class OutputNode():
    def __init__(self):
        self.input = []
        self.weight = initList(HIDDENNODENUMBER)

    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

    def updateWeightNew(self, prosInput):
        self.weight, deltalist = updateOutputWeight(self.input, self.weight, self.getOutputNew(), prosInput, ANNSTEP)
        return deltalist

    def updateInput(self, input):
        self.input = [1.0] + input

class Sample:
    def __init__(self):
        self.user_id = -1
        self.brand_id = -1
        self.operatorList = []
        self.supervisor = -1

def loadData(filePath, sampleCollection):
    sampleFile = open(filePath, "r")
    for line in sampleFile.readlines():
        lineSplit = line[:-1].split(",")
        sample = Sample()
        sample.user_id = int(lineSplit[0])
        sample.brand_id = int(lineSplit[1])
        
        for i in xrange(4):
            sample.operatorList.append(int(lineSplit[2+i]))
        sample.supervisor = int(lineSplit[6])
        sampleCollection.append(sample)
    sampleFile.close()

def mainProcess():
    initSampleSource = "../data/samples"
    errorLogsource = "../data/errlog"
    hiddenWeightSource = "../data/hidden"
    outputWeightSource = "../data/output"
    errorLogFile = open(errorLogsource, "w")
    hiddenWeightFile = open(hiddenWeightSource, "w")
    outputWeightFile = open(outputWeightSource, "w")

    initSampleFile = open(initSampleSource, "r")
    sampleCount = len(initSampleFile.readlines())
    initSampleFile.close()

    initSamples = []
    hiddenList = []
    
    loadData(initSampleSource, initSamples)

    for m in xrange(HIDDENNODENUMBER):
        hiddenNode = HiddenNode()
        hiddenList.append(hiddenNode)

    outputNode = OutputNode()

    updateTime = 0
    while updateTime < MAXTIME:
        E = 0
        updateTime += 1
        print "time %d" % int(updateTime)
        startTime = time.time()

        for i in xrange(sampleCount):
            for j in xrange(HIDDENNODENUMBER):
                hiddenList[j].updateInput(initSamples[i].operatorList)
            
            outputNode.updateInput([hiddennode.getOutputNew() for hiddennode in hiddenList])
            deltaList = outputNode.updateWeightNew(initSamples[i].supervisor)

            for t in xrange(HIDDENNODENUMBER):
                hiddenList[t].updateWeightNew(deltaList[t], outputNode.weight[t])

            outputNode.updateInput([hiddennode.getOutputNew() for hiddennode in hiddenList])
            finaloutput = outputNode.getOutputNew()

            E += (float(finaloutput) - float(initSamples[i].supervisor))**2

        E = float(E)/2
        print 'E is %f' % float(E)
        print time.time() - startTime
        
        errorLogFile.write(str(E)+"\n")

        if E < ANNPRECISION:
            break
        else:
            pass

    for i in xrange(len(hiddenList)):
        for item in hiddenList[i].weight:
            hiddenWeightFile.write(str(item)+"\n")
    hiddenWeightFile.close()

    for item in outputNode.weight:
        outputWeightFile.write(str(item)+"\n")
    outputWeightFile.close()

if __name__ == '__main__':
    mainProcess()
