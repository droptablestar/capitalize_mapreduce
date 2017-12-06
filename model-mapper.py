#!/usr/bin/python

import sys

# this will be our features dictionary
features = {}
LOWER = 1
UPPER = 0
for line in sys.stdin:
    line = line.strip('\n').split()
    for word in line:
        isLower = word.islower()
        length = len(word)

        # break the work into features depending on its length
        if length > 3: ft = [word,word[-2:],word[-3:],word[:2],word[:3]]
        elif length==3: ft = [word,word[-2:],word[:2]]
        else: ft = [word]

        ft = map(lambda x: x.lower(),ft)
        # insert the words features into the dictionary
        # or create a new location in the dictionary for the feature
        for d in ft:
            if d in features: 
                if isLower: features[d][LOWER] += 1
                else: features[d][UPPER] += 1                
            else:
                if isLower: features[d] = [0,1]
                else: features[d] = [1,0]
    # flush the dictionary at 10000 elements
    if len(features) > 10000:
        for k in features:
            print '%s\t%f\t%f' % \
                (k,features[k][UPPER],features[k][LOWER])
        features.clear()
# flush the remainder of the dictionary
for k in features:
    print '%s\t%f\t%f' % (k,features[k][UPPER],features[k][LOWER])
