#!/usr/bin/python

import sys
fVector = {}

LOWER = 2
UPPER = 1
# this value is the minimum number of times we need to see a word
# for it to be allowed to remain in our calculations
THRESHOLD = 1000

# determines the probability a feature is uppercase
def prob(f):
    pfU = f[UPPER-1] / (f[UPPER-1]+f[LOWER-1])
    if pfU == 0: pfU = 0.01
    return pfU

prevWord = ''
# [#timesUpper, #timesLower]
word = [0,0]

for line in sys.stdin:
    line = line.strip()
    line = line.split('\t')
    line = map(lambda x: x.strip(),line)
    key = line[0]

    # still on the same word, or at the beginning of the loop
    if key == prevWord or prevWord == '':
        word[LOWER-1] += float(line[LOWER])
        word[UPPER-1] += float(line[UPPER])
        prevWord = key
    # we've moved on to a new word. if its count is less than the
    # threshold dont print it. otherwise print
    # [word,#timesUpper,#timesLower,p(upper)]
    else:
        if word[UPPER-1] <= THRESHOLD and word[LOWER-1] == 0\
            or word[UPPER-1] == 0 and word[LOWER-1] <= THRESHOLD:
            word = [float(line[UPPER]),float(line[LOWER])]
            prevWord = key
            continue
        print '%s\t%d\t%d\t%f' % \
            (prevWord,word[UPPER-1],word[LOWER-1],prob(word))
        word = [float(line[UPPER]),float(line[LOWER])]
        prevWord = key
print '%s\t%d\t%d\t%f' % \
    (prevWord,word[UPPER-1],word[LOWER-1],prob(word))
