import MySQLdb

try:
    connection = MySQLdb.connect(host="localhost", user="root", passwd="", port=3306)
    cursor = connection.cursor()

    cursor.execute('create database if not exists tianchi')
    connection.select_db('tianchi')
    cursor.execute('create table if not exists initdata(id int AUTO_INCREMENT, user_id int, brand_id  int, operator int, time int, PRIMARY KEY(id))')
    connection.commit()
    cursor.close()
    connection.close()

except MySQLdb.Error, e:
    print "mysql error %d: %s" % (e.args[0], e.args[1])
