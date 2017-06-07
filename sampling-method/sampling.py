# encoding=utf-8

import sys
import math
import random
import time
import numpy as np

SAMPLE_MAX_COUNT = 100000

def fair_die(n):
    return int(np.floor(np.random.rand() * n))

LEN = 1000  # LCM is best
loaded_die_table = []

def loaded_die_init(probs):
    psum = np.zeros(len(probs))
    s = 0
    for i, p in enumerate(probs):
        s += p
        psum[i] = s

    loaded_die_table = np.zeros(LEN)
    b = 0
    for a in range(0, LEN):
        if float(a+1) / LEN <= psum[b] + 1e-5:
            loaded_die_table[a] = b
        else:
            b += 1

def loaded_die_rand():
    x = random.random()
    return loaded_die_table[ x * LEN ]

def biased_coin(p):
    x = random.random();
    return 1 if x<p else 0

def fair_die_with_biased_coins(n):
    for i in range(0, n):
        x = random.random()
        if x < 1.0 / (n - i): # bias coin with p = 1.0 / (n-i)
            return i

def loaded_die_with_biased_coin(probs):
    ''' O(M*N) '''
    n = len(probs)
    mass = 1.0
    for i, p in enumerate(probs):
        x = random.random()
        if x < p / mass:
            return i
        mass = mass - p

def roulette_wheel_selection_init(probs):
    psum = np.zeros(len(probs))
    s = 0.0
    for i, p in enumerate(probs):
        s += p
        psum[i] = s
    return psum

def binary_search(lst, value):  
    mid, low, high = 0, 0, len(lst)-1
    while low <= high:  
        mid = (low + high) / 2
        if lst[mid] < value-1e-4:
            low = mid + 1
        elif lst[mid] > value+1e-4:
            high = mid - 1
        else:
            return mid
    return low

def roulette_wheel_selection_gen(psum):
    ''' O(M*log(N)) '''
    x = random.random()
    i = binary_search(psum, x) # find the index i of the smallest element in A larger than x.
    return i

def fair_die_biased_coin_loaded_die(probs):
    ''' 虽然满足分布，但是会miss太多，导致效率较低 '''
    n = len(probs)
    i = random.randint(0, n-1)    # 1/n to index i
    y = random.random()
    if y < probs[i]:
        return i    # 1/n * probs[i] to i
    else:
        return -1   # miss

def check_sum(probs):
    psum = 0.0
    for p in probs:
        psum += p
    return True if psum > 1-1e-4 else False

def alias_setup(probs):
    '''
    Compute utility lists for non-uniform sampling from discrete distributions.
    Refer to https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
    for details
    '''
    K = len(probs)
    q = np.zeros(K)
    J = np.zeros(K, dtype=np.int)

    smaller = []
    larger = []
    for kk, prob in enumerate(probs):
        q[kk] = K*prob
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)

    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large
        q[large] = q[large] + q[small] - 1.0
        if q[large] < 1.0:
            smaller.append(large)
        else:
            larger.append(large)

    return J, q

def alias_draw(J, q):
    '''
    Draw sample from a non-uniform discrete distribution using alias sampling.
    '''
    K = len(J)

    kk = int(np.floor(np.random.rand()*K))
    if np.random.rand() < q[kk]:
        return kk
    else:
        return J[kk]

def test_fair_die(n):
    t = np.zeros(n)
    start = time.time()
    for i in range(0, SAMPLE_MAX_COUNT):
        x = fair_die(n)
        t[x] += 1
    end = time.time()
    print "spend time: ", end - start
    for i in range(0, n):
        print t[i]

def test_fair_die_with_biased_coins(n):
    t = np.zeros(n)
    start = time.time()
    for i in range(0, SAMPLE_MAX_COUNT):
        x = fair_die_with_biased_coins(n)
        t[x] += 1
    end = time.time()
    print "spend time: ", end - start
    for i in range(0, n):
        print t[i]

def test_loaded_die_with_biased_coin(probs):
    n = len(probs)
    t = np.zeros(n)
    start = time.time()
    cnt = 0
    while(cnt < SAMPLE_MAX_COUNT):
        x = loaded_die_with_biased_coin(probs)    # 1
        if x >= 0 and x < n:
            t[x] += 1
            cnt += 1
    end = time.time()
    print "spend time: ", end - start
    # for i in range(0, n):
    #     print t[i]

def test_roulette_wheel_selection_gen(probs):
    n = len(probs)
    t = np.zeros(n)
    psum = roulette_wheel_selection_init(probs)   # 3
    start = time.time()
    cnt = 0
    while(cnt < SAMPLE_MAX_COUNT):
        x = roulette_wheel_selection_gen(psum)    # 3
        if x >= 0 and x < n:
            t[x] += 1
            cnt += 1
    end = time.time()
    print "spend time: ", end - start
    # for i in range(0, n):
    #     print t[i]

def test_alias_method(probs):
    n = len(probs)
    t = np.zeros(n)
    J, q = alias_setup(probs)  # 2
    start = time.time()
    cnt = 0
    while(cnt < SAMPLE_MAX_COUNT):
        x = alias_draw(J, q)                      # 2
        if x >= 0 and x < n:
            t[x] += 1
            cnt += 1
    end = time.time()
    print "spend time: ", end - start
    # for i in range(0, n):
    #     print t[i]

def test_fair_die_biased_coin_loaded_die(probs):
    n = len(probs)
    t = np.zeros(n)
    start = time.time()
    cnt = 0
    while(cnt < SAMPLE_MAX_COUNT):
        x = fair_die_biased_coin_loaded_die(probs)  # 4
        if x >= 0 and x < n:
            t[x] += 1
            cnt += 1
    end = time.time()
    print "spend time: ", end - start
    # for i in range(0, n):
    #     print t[i]

if __name__ == "__main__":

    # print "================test_fair_die=============="
    # test_fair_die(4)
    # print "================test_fair_die_with_biased_coins=============="
    # test_fair_die_with_biased_coins(4)

    data = np.zeros(1000)
    sumdata = 0.0
    for i in range(0, 1000):
        data[i] = random.randint(0, 10000)
        sumdata += data[i]
    for i in range(0, 1000):
        data[i] = data[i] / sumdata

    probs = data
    if not check_sum(probs):
        print "sum of probs is not 1"
        n = len(probs)
        sump = 0.0
        for i in range(0, n):
            sump += probs[i]
        for i in range(0, n):
            probs[i] = probs[i] / sump
        print ",".join([str(p) for p in probs])

    print "======test_loaded_die_with_biased_coin======"
    test_loaded_die_with_biased_coin(probs)
    print "======test_roulette_wheel_selection_gen======"
    test_roulette_wheel_selection_gen(probs)
    print "======test_alias_method======"
    test_alias_method(probs)
    print "======test_fair_die_biased_coin_loaded_die======"
    test_fair_die_biased_coin_loaded_die(probs)

'''
Result:
$ python sampling.py
======test_loaded_die_with_biased_coin======
spend time:  27.368999958
======test_roulette_wheel_selection_gen======
spend time:  0.494000196457
======test_alias_method======
spend time:  0.302999973297
======test_fair_die_biased_coin_loaded_die======
spend time:  180.98300004
'''