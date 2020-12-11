# -*- coding: utf-8 -*-
"""
Created on Wed Dec  10 12:13:42 2020

@author: GFL
"""

import numpy as np
def count_1_and_3(numbers):
    # Put the plugs in the right order and find the number of 1 and 3 diffs
    ln = np.array([0] + sorted(numbers) + [max(numbers)+3])
    ld = list(np.diff(ln))
    return ld.count(1), ld.count(3)

test_data = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

testnumbers = list(map(int,test_data.split()))

assert (22,10) == count_1_and_3(testnumbers), "Test case part1 failed"

with open("d10_pt1.txt") as f:
    numbers = list(map(int,f.readlines()))

n1, n3 = count_1_and_3(numbers)
ans1 = n1 * n3
print(f"Answer part 1: {ans1}")


#%% Part 2
# Adapters can always be 

simple_test_data = """16
10
15
5
1
11
7
19
6
12
4"""
simple = list(map(int,simple_test_data.split()))

def count_valid_ways(numbers):
    ln = np.array([0] + sorted(numbers) + [max(numbers)+3])
#    print(ln)
    ld = list(np.diff(ln))
    # there are only differences of 1 and 3
    # manual analysis; chain of 2 1's is *2
    # chain of 3 1's is x3
    # chain of 4 1's is x9
    n_opts = 1 # the full sequence
#    print(ld)
    c = 0
    for i,d in enumerate(ld):
        if d == 1:
            c += 1
        else:
#            print(f"i={i}, chain of {c} ld: {ld[i-c-1:i+1]}")
            if c == 2:
                n_opts *= 2
            elif c == 3:
                n_opts *= 4
            elif c == 4:
                n_opts *= 7
            c = 0
    return n_opts

def analyse_chain(numbers):
    ln = np.array([0] + sorted(numbers) + [max(numbers)+3])
#    print(ln)
    ld = list(np.diff(ln))
    chains1 = []
    c = 0
    for d in ld:
        if d == 1:
            c += 1
        else:
            chains1.append(c)
            c = 0
    print(chains1)

#analyse_chain(simple)
#analyse_chain(testnumbers)
#analyse_chain(numbers)

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


assert 8 == count_valid_ways(simple), "Simple test case failed"

assert 19208 == count_valid_ways(testnumbers), "Medium test case failed"

ans2 = count_valid_ways(numbers)
print(f"Answer part 2: {ans2}")












