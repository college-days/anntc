finalFile = open("../data/samples", "w")
initOne = open("../data/0i", "r")
initTwo = open("../data/1i", "r")
initThree = open("../data/2i", "r")

for line in initOne:
    finalFile.write(line)
initOne.close()

for line in initTwo:
    finalFile.write(line)
initTwo.close()

for line in initThree:
    finalFile.write(line)
initThree.close()

finalFile.close()
