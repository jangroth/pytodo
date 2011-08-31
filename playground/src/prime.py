#! /usr/bin/python
from math import sqrt
import time

def printPrimes(max):
    start = time.time()
    checkValues = [2]
    for x in range(3, max, 2):
        for y in checkValues:
            if x % y == 0:
                break
        else:
            #print 'found ', n
            checkValues.append(x)

    elapsed = time.time() - start

    print max, ' in ', elapsed  
    return checkValues      
    
print printPrimes(100000)
