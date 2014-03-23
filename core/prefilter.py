# -*- coding: UTF-8 -*-
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

resource = open("./data/t_alibaba_data.csv", "r")
one= open("./data/0", "w")
two = open("./data/1", "w")
three = open("./data/2", "w")
four = open("./data/3", "w")
twobuy = open("./data/1b", "w")
threebuy = open("./data/2b", "w")
fourbuy = open("./data/3b", "w")
aprildaylist = []
maydaylist = []
junedaylist = []
julydaylist = []
augustdaylist = []

try:
    connection = MySQLdb.connect(host="localhost", user="root", passwd="", db="tianchi", port=3306)
    cursor = connection.cursor()

    for line in resource:
        user_id, brand_id, operator, time = line[:-1].split(",")
        if user_id != "user_id":
            time = time.decode("gbk")
            timelist = time.split("月")
            month = timelist[0]
            day = timelist[1].replace("日", "")
            
            month = month.encode("utf-8")
            try:
                month = int(month)
            except:
                pass
            
            day = day.encode("utf-8")
            try:
                day = int(day)
            except:
                pass

            if month == 4:
                aprildaylist.append(day)
            if month == 5:
                maydaylist.append(day)
            if month == 6:
                junedaylist.append(day)
            if month == 7:
                julydaylist.append(day)
            if month == 8:
                augustdaylist.append(day)
            
            if month == 4:
                one.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(0)))
            elif month == 5 and day < 16:
                one.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(0)))
            elif month == 5 and day >=16:
                two.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(1)))
                if int(operator) == 1:
                    twobuy.write(user_id+","+brand_id+","+operator+"\n")
            elif month == 6 and day < 16:
                two.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(1)))
                if int(operator) == 1:
                    twobuy.write(user_id+","+brand_id+","+operator+"\n")
            elif month == 6 and day >= 16:
                three.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(2)))
                if int(operator) == 1:
                    threebuy.write(user_id+","+brand_id+","+operator+"\n")
            elif month == 7 and day < 16:
                three.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(2)))
                if int(operator) == 1:
                    threebuy.write(user_id+","+brand_id+","+operator+"\n")
            elif month == 7 and day >= 16:
                four.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(3)))
                if int(operator) == 1:
                    fourbuy.write(user_id+","+brand_id+","+operator+"\n")
            elif month == 8:
                four.write(user_id+","+brand_id+","+operator+"\n")
                cursor.execute('insert into initdata (`user_id`, `brand_id`, `operator`, `time`) values(%d, %d, %d, %d)' % (int(user_id), int(brand_id), int(operator), int(3)))
                if int(operator) == 1:
                    fourbuy.write(user_id+","+brand_id+","+operator+"\n")
            else:
                pass
            print 'commit %d, %d, %d' % (int(user_id), int(brand_id), int(operator))
            connection.commit()
        else:
            pass

    print '4----------------'
    print min(aprildaylist)
    print max(aprildaylist)
    print '-----------------'
    print '5----------------'
    print min(maydaylist)
    print max(maydaylist)
    print '-----------------'
    print '6----------------'
    print min(junedaylist)
    print max(junedaylist)
    print '-----------------'
    print '7----------------'
    print min(julydaylist)
    print max(julydaylist)
    print '-----------------'
    print '8----------------'
    print min(augustdaylist)
    print max(augustdaylist)
    print '-----------------'

    
    cursor.close()
    connection.close()
    resource.close()
    one.close()
    two.close()
    three.close()
    four.close()
    twobuy.close()
    threebuy.close()
    fourbuy.close()

except MySQLdb.Error, e:
    print "mysql error %d: %s" % (e.args[0], e.args[1])
