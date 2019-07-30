mydata = 5

def f1():
    for a in range(mydata):
        a=mydata+1

import timeit

print(timeit.timeit("f1", setup = "from __main__ import f1", number=1000))