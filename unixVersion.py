#!/usr/bin/python

import sys,io
from random import random

# this will be our features dictionary
features = {}
get = features.get

# the minimum times a feature must be seen to remain in the dictionary
THRESHOLD = 0

# how far apart prob's need to be to check sums
DISTANCE = 0.01

# determines the distance the sums have to be to do a coin toss
TOSSDISTANCE = 500

# determines the weight of the weighted coin toss
# for determining case when prob's are close
TOSS = 0.66

# takes a word
# returns a list [word,feature1,#timesUpper1,#timesLower1,p(U)1,...]
# if the feature doens't exist a None is returned in its place
def makeVector(t):
    if t=='':
        return [[0]]
    if len(t) > 3:
        return [t,get(t),get(t[-2:]),get(t[-3:]),get(t[:2]),get(t[:3])]
    elif len(t) == 3:
        return [t,get(t),get(t[:2]),get(t[2:])]
    else:
        return [t,get(t)]

# takes the counts as a list
# returns the probability this feature is uppercase
def prob(f):
    pfU = float(f[0]) / (float(f[0])+float(f[1]))
    if pfU == 0: pfU = 0.1
    return pfU

# model-mapper.py
# contruct feature dictionary and count occurances of each feature
with open(sys.argv[1],'r') as f:
    
    for line in f:
        line = line.strip('\n').split()
        for word in line:
            isLower = word.islower()
            length = len(word)

            # break word into features depending on its length
            if length > 3: ft = [word,word[-2:],word[-3:],word[:2],word[:3]]
            elif length==3: ft = [word,word[-2:],word[:2]]
            else: ft = [word]

            ft = map(lambda x: x.lower(),ft)
            # insert every feature into the dictionary or create a new
            # key -> value pair
            for d in ft:
                if d in features: 
                    if isLower: features[d][1] += 1
                    else: features[d][0] += 1                
                else:
                    if isLower: features[d] = [0,1]
                    else: features[d] = [1,0]

# model-reducer.py
# remove values which haven't appeared more than THRESHOLD times
# calculate probabilities of each feature
toRemove = []
for f in features:
    if features[f][0] <= THRESHOLD and features[f][1] == 0\
            or features[f][0] == 0 and features[f][1] <= THRESHOLD:
        toRemove.append(f)
        continue
    features[f] += [prob(features[f])]

for f in toRemove: del features[f]

with open('featuresUnix','w') as f:
    for k in features:
        f.write(k+'\t')
        for v in features[k]:
            f.write(str(v)+'\t')
        f.write('\n')
    
# break line into feature vector
for line in sys.stdin:
    line = line.strip()
    vListL = [makeVector(line)]

    newString = ''

    # part4-reducer.py
    # run classifier on the test data
    for lower in vListL:
        weightLower = weightUpper = False

        lower = filter(lambda x: x!=None,lower)
        # this lien has no features 
        if len(lower) < 2:
            if lower[0] != [0]:
                print lower[0],
            continue
        # get the probabilites for each feature out of the lines
        lowerP = [1 - float(lower[i][2]) for i in range(1,len(lower))]
        upperP = [float(lower[i][2]) for i in range(1,len(lower))]

        # multiple all the probabilities together
        pL = reduce(lambda x,y: x*y,lowerP)
        pU = reduce(lambda x,y: x*y,upperP)

        # check if the two probabilities are close 
        if abs(pU - pL) < DISTANCE:
            # get the amount of times we've seen all the features of this word
            # in each case
            sumL = reduce(lambda x,y: x+y, map(lambda x: x[1],lower[1:]))
            sumU = reduce(lambda x,y: x+y, map(lambda x: x[0],lower[1:]))

            # if the sum are close do a 'weighted coin toss' to determing case
            # weighted more towards the higher prob
            if abs(sumL - sumU) < TOSSDISTANCE:
                toss = random()
                if pU > pL:
                    if toss < TOSS: newString += lower[0].capitalize().strip() + ' '
                    else: newString += lower[0].strip() + ' '
                else:
                    if toss < TOSS: newString += lower[0].strip() + ' '
                    else: newString += lower[0].capitalize().strip() + ' '
            else:
                if sumL < sumU: newString += lower[0].capitalize() + ' '
                else: newString += lower[0] + ' '

        # get the case of the word from the higher prob
        else:
            if pL < pU: newString += lower[0].capitalize() + ' '
            elif pL > pU: newString += lower[0] + ' '

    # print lower
    # print pU,pL
    print '%s' % newString.strip()
