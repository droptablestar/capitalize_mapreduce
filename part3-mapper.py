#!/usr/bin/python

import sys

features = {}
words = []
get = features.get

def makeVector(t):
    # get the feature tuples from the features dict
    # None is returned for a feature thats not known
    if t=='':
        return [[0]]
    if len(t) > 3:
        return [t,get(t),get(t[-2:]),get(t[-3:]),get(t[:2]),get(t[:3])]
    elif len(t) == 3:
        return [t,get(t),get(t[:2]),get(t[2:])]
    else:
        return [t,get(t)]

# parse features file
f = open('features','r')
lines = f.readlines()
f.close()

# split lines into [word,#timesUpper,#timesLower,probUpper]
# reconstruct the trained feature dictionary
length = len(lines)
for i in xrange(length):
    lines[i] = lines[i].strip('\n').split('\t')
    p = [lines[i][0]]
    p += [float(j) for j in lines[i][1:]]
    features[lines[i][0]] = p

for line in sys.stdin:
    line = line.strip()
    # split each word into a feature vector
    # break line into features
    if line == '':
        word=[makeVector('')]
    else:
        for w in line.split():
            word=[makeVector(w)]

    # output the feature vectors for this test word
    for i in word:
        print '%s\t' % i[0],
        i = filter(lambda x: x!=None,i)
        for j in range(1,len(i)):
            for k in i[j][1:]:
                print '%s\t' % k,
    print
