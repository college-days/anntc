import os
import math
from calcUtil import getNetOutput
import MySQLdb

INPUTNODENUMBER = 4
HIDDENNODENUMBER = 2

class HiddenNode():
    def __init__(self, input, params):
        self.input = [1.0] + input
        self.weight = params

    def getOutputNew(self):
        return getNetOutput(self.input, self.weight)

    def updateWeightNew(self, delta, weight):
        self.weight = updateHiddenWeight(self.input, self.weight, self.getOutputNew(), ANNSTEP, delta, weight)

    def updateInput(self, input):
        self.input = [1.0] + input

class OutputNode():
    def __init__(self, input, params):
        self.input = [1.0] + input
        self.weight = params

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


class Verify:
    def __init__(self):
        self.hiddenParam = self.loadHiddenParam()
        self.outputParam = self.loadOutputParam()
        self.hiddenNodeList = []

    def decision(self, target):
        for i in xrange(len(self.hiddenParam)):
            hiddennode = HiddenNode(target, self.hiddenParam[i])
            self.hiddenNodeList.append(hiddennode)
        
        outputnode = OutputNode([hidden.getOutputNew() for hidden in self.hiddenNodeList], self.outputParam)
        result = outputnode.getOutputNew()
        self.hiddenNodeList = []
        #print result
        if result > 0.5:
            #print 'yes'
            return True
        else:
            #print 'no'
            return False

    def loadHiddenParam(self):
        hiddenSource = "../data/hidden" 
        hiddenFile = open(hiddenSource, "r")
        hiddenParamList = []
        for line in hiddenFile.readlines():
            hiddenParamList.append(float(line[:-1]))
        hiddenFile.close()
    
        hiddenParams = []
        hiddenParams.append(hiddenParamList[0:5])
        hiddenParams.append(hiddenParamList[5:10])

        return hiddenParams

    def loadOutputParam(self):
        outputSource = "../data/output"
        outputFile = open(outputSource, "r")
        outputParam = []
        for line in outputFile.readlines():
            outputParam.append(float(line[:-1]))
        outputFile.close()

        return outputParam

def getConnection():
    try:
        connect = MySQLdb.connect(host='localhost', user='root', passwd='', db='tianchi', port=3306)
        return connect
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def initUniqueList():
    useridList = []
    brandidList = []

    connect = getConnection()
    cursor = connect.cursor()
    cursor.execute('select user_id from initdata')
    useridList = cursor.fetchall()
    useridList = [int(item[0]) for item in useridList]
    cursor.execute('select brand_id from initdata')
    brandidList = cursor.fetchall()
    brandidList = [int(item[0]) for item in brandidList]
    cursor.close()
    connect.close()
    #return list(set(useridList)), list(set(brandidList))
    return list(set(useridList))
 
if __name__ == '__main__':
    useridList = initUniqueList()

    verify = Verify()
    resultFile = open("../data/cleantha.txt", "w")

    connect = getConnection()
    cursor = connect.cursor()
 
    brandMap = {}

    for userid in useridList:
        brandidList = []
        cursor.execute('select distinct brand_id from initdata where user_id=%d and time=%d' % (int(userid), int(3)))
        brandidList = cursor.fetchall()
        brandidList = [int(item[0]) for item in brandidList]
        if len(brandidList) != 0:
            resultFile.write(str(userid)+"\t")
        for brandid in brandidList:
            #print 'yeah'
            operatorList = []
            cursor.execute('select operator from initdata where user_id=%d and brand_id=%d and time=%d' % (int(userid), int(brandid), int(3)))
            operatorList = cursor.fetchall()
            operatorList = [int(item[0]) for item in operatorList]
            operatorTrainList = []
            for i in xrange(4):
                operatorTrainList.append(operatorList.count(i))
            result = verify.decision(operatorTrainList)
            if result:
                print userid, brandid
                resultFile.write(str(brandid)+",")
        resultFile.write("\n")

    resultFile.close()
