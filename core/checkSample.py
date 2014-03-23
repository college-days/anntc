file = open("../data/samples", "r")
for line in file.readlines():
    print line[:-1]

file.close()
