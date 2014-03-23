import MySQLdb


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
    
def getSample(useridList, timeflag):
    initFile = open("./data/"+str(timeflag)+"i", "w")
    
    connect = getConnection()
    cursor = connect.cursor()
    
    brandMap = {}

    for userid in useridList:
        brandidList = []
        cursor.execute('select distinct brand_id from initdata where user_id=%d and time=%d' % (int(userid), int(timeflag)))
        brandidList = cursor.fetchall()
        brandidList = [int(item[0]) for item in brandidList]
        for brandid in brandidList:
            initFile.write(str(userid)+","+str(brandid))
            print timeflag, userid, brandid
            operatorList = []
            #for i in xrange(4):
            #    cursor.execute('select count(*) from initdata where user_id=%d and brand_id=%d and operator=%d and time=%d' % (int(userid), int(brandid), int(i), int(timeflag)))
            #    operator = cursor.fetchone()
            #    operator = int(operator[0])
            #    operatorList.append(operator)
            cursor.execute('select operator from initdata where user_id=%d and brand_id=%d and time=%d' % (int(userid), int(brandid), int(timeflag)))
            operatorList = cursor.fetchall()
            operatorList = [int(item[0]) for item in operatorList]
            for i in xrange(4):
                initFile.write(","+str(operatorList.count(i)))
            cursor.execute('select count(*) from initdata where user_id=%d and brand_id=%d and operator=1 and time=%d' % (int(userid), int(brandid), int(timeflag+1)))
            isBuy = cursor.fetchone()
            isBuy = int(isBuy[0])
            if isBuy != 0:
                initFile.write(","+str(1))
            else:
                initFile.write(","+str(0))
            initFile.write("\n")

    initFile.close()
    cursor.close()
    connect.close()

if __name__ == '__main__':
    useridList = initUniqueList()
    for i in xrange(3):
        getSample(useridList, i)
