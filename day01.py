#!/Users/geert/opt/anaconda3/bin/python3


def find_pair_sum(l,s=2020):
    # return the two items in <l> that sum up to <s>
    for i1,a1 in enumerate(l):
        for i2,a2 in enumerate(l):
            if i1 == i2:
                continue
            if a1 + a2 == s:
                return [a1,a2]

def find_triplet_sum(l,s=2020):
    # return the triplet in <l> that sum up to <s>
    for i1,a1 in enumerate(l):
        for i2,a2 in enumerate(l):
            if i1 == i2:
                continue
            for i3,a3 in enumerate(l):
                if i3 == i1 or i3 == i2:
                    continue
                if a1 + a2 + a3 == s:
                    return [a1,a2,a3]

if __name__ == "__main__":

    from aoc_utils import load_ints

    test_data = load_ints("input/d1_test.txt")
    test_answer = 514579
    a = find_pair_sum(test_data)
    assert a[0] * a[1] == test_answer, "test case wrong"
    
    # actual case
    data = load_ints("input/d01_p1.txt")
    a = find_pair_sum(data)
    ans = a[0] * a[1]
    print(f"Answer pt1:  {ans}")
    
    # Part 2
    a = find_triplet_sum(test_data)
    t2_answer = 241861950
    ans = a[0] * a[1] * a[2]
    assert t2_answer == ans, "test case 2 wrong"
    
    a = find_triplet_sum(data)
    ans = a[0] * a[1] * a[2]
    print(f"Answer pt2: {ans}")