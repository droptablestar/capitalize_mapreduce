import sys

f = open(sys.argv[1])
resultsFile = map(lambda x: x.strip(' \n'), f.readlines())
f.close()

f = open(sys.argv[2])
truthFile = map(lambda x: x.strip(' \n'), f.readlines())
f.close()

wrong = 0
for i in range(len(resultsFile)):
    if len(resultsFile[i]) < 1: wrong +1
    elif resultsFile[i][0] != truthFile[i][0]:
        wrong += 1
        
print wrong
print (1 - wrong / 932.0) * 100
