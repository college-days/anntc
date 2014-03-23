import time

def filterData(iter):
    if iter != 3:
        superviseSource = "./data/"+str(iter+1)+"b"
        superviseList = []
        superviseFile = open(superviseSource, "r")
        for line in superviseFile.readlines():
            lineSplit = line.split(",")
            userid = lineSplit[0]
            brandid = lineSplit[1]
            flag = str(userid)+":"+str(brandid)
            superviseList.append(flag)

    filePath = "./data/"+str(iter)
    savePath = "./data/"+str(iter)+"i"
    file = open(filePath, "r")
    saveFile = open(savePath, "w")
    userMap = {}
    for line in file.readlines():
        lineSplit = line[:-1].split(",")
        user_id = int(lineSplit[0])
        brand_id = int(lineSplit[1])
        operator = int(lineSplit[2])
        if user_id not in userMap.keys():
            userMap[user_id] = {brand_id: [operator]}
        else:
            if brand_id not in userMap[user_id].keys():
                userMap[user_id][brand_id] = [operator]
            else:
                userMap[user_id][brand_id].append(operator)
    for userKey, userValue in userMap.items():
        for brandKey, brandValue in userMap[userKey].items():
            saveFile.write(str(userKey)+",")
            saveFile.write(str(brandKey)+",")
            userMap[userKey][brandKey] = list(set(userMap[userKey][brandKey]))
            operatorList = []
            for operatorType in xrange(4):
                if operatorType in userMap[userKey][brandKey]:
                    operatorList.append(1)
                else:
                    operatorList.append(0)
            for value in operatorList:
                saveFile.write(str(value)+",")
            if iter != 3:
                flag = str(userKey)+":"+str(brandKey)
                if flag not in superviseList:
                    saveFile.write(str(0))
                else:
                    print 'yeah'
                    saveFile.write(str(1))
                saveFile.write("\n")
    
    saveFile.close()
    file.close()

if __name__ == '__main__':
    for i in xrange(4):
        filterData(i)
