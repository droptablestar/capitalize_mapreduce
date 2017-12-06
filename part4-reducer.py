#!/usr/bin/python
import sys
from random import random

# This is the difference in probabilities that will cause
# us to check the counts and perhaps do a coin toss
DISTANCE = 0.01

# the difference in amounts of times we've seen each word required
# to do a coin toss
TOSSDISTANCE = 500

# weight of the coin
TOSS = 0.66

for line in sys.stdin:
    weightLower = weightUpper = False
    line = line.strip()
    line = line.split('\t')

    # this is a word with no features
    if len(line)  == 1:
        if line[0][1] == '0': print
        else: print line[0]
        continue

    lower = line
    word = lower[0]

    # get the probabilities out of the line
    lowerP = [1 - float(lower[i]) for i in range(3,len(lower),3)]
    upperP = [float(lower[i]) for i in range(3,len(lower),3)]

    # calculate the probabilities
    pL = reduce(lambda x,y: x*y,lowerP)
    pU = reduce(lambda x,y: x*y,upperP)

    # check the difference between the probabilities for further analysis
    if abs(pU - pL) < DISTANCE :
        sumL = reduce(lambda x,y: x+y, [float(lower[i]) for i in range(2,len(lower),3)])
        sumU = reduce(lambda x,y: x+y, [float(lower[i]) for i in range(1,len(lower),3)])

        # if the sum are close do a 'weighted coin toss' to determing case
        # weighted more towards the higher prob
        if abs(sumL - sumU) < TOSSDISTANCE:
            toss = random()
            if pU > pL:
                if toss < TOSS: case = word.capitalize()
                else: case = word
            else:
                if toss < TOSS: case = word
                else: case = word.capitalize()
        else:
            if sumL < sumU: case = word.capitalize()
            else: case = word
    else:
        if pU > pL: case = word.capitalize()
        elif pU < pL: case = word

    # print lower
    # print upper
    # print pU,pL
    print '%s' % case
