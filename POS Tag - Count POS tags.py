# Preamble
import nltk 
import string
import numpy as np
import os
import sys

f = os.path.join(sys.path[0], '1207 Manually improved tagged sent - 314 msgs.txt')
# Manually tagged until the 314th sentence.





# Convert from string fly/VB to list of tuples [('fly, 'VB')], and count tags
total = 0
CHN = 0
CHV = 0
CHU = 0
CHY = 0
CHI = 0
CHO = 0


with open(f) as tagfile:
    f1 = tagfile.readlines()
    for line in f1:
        x=[nltk.tag.str2tuple(t) for t in line.split()]
        for a in x:
            total += 1
            if a[1] == 'CHN':
                CHN += 1
            if a[1] == 'CHV':
                CHV += 1
            if a[1] == 'CHU':
                CHU += 1
            if a[1] == 'CHY':
                CHY += 1
            if a[1] == 'CHI':
                CHI += 1
            if a[1] == 'CHO':
                CHO += 1
            
    print (total, CHN, CHV, CHU, CHY, CHI, CHO)