#!/Users/geert/opt/anaconda3/bin/python3

def find_error(numbers,n):
    # Find which number in the list <numbers> is not the sum of two numbers in the
    # preceding <n> numbers. (skip first <n>)
    for i,a in enumerate(numbers[n:]):
        #print(i+n,a)
        ok = False
        for a1 in numbers[i:i+n]:
            for a2 in numbers[i+1:i+n]:
                if a1+a2 == a:
                    ok = True
                    break
            if ok:
                break
        if not ok:
            return a

def find_contiguous_sum(numbers, s, n):
    for i0 in range(len(numbers)):
#        print(i0,end=" ")
        for i1 in range(i0+1,len(numbers)):
            v = numbers[i0:i1+1]
#            print(f"Check {i0}-{i1}, v={v}")
            if sum(v) == s:
                print(v)
                return min(v) + max(v)
            elif sum(v) > s:
#                print(f"Aborted for {i0}-{i1}")
                break
#        print(f"Did not find for {i0}")
        

if __name__ == "__main__":
    test_data = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

    testnumbers = list(map(int,test_data.split()))

    assert 127 == find_error(testnumbers, 5), "Test case part1 failed"
    
    from aoc_utils import load_ints
    numbers = load_ints("input/d09_pt1.txt")
    
    ans1 = find_error(numbers, 25)
    print(f"Answer part 1: {ans1}")


    # Part 2: find contiguous range of numbers that is equal to <ans1>
    assert 62 == find_contiguous_sum(testnumbers, 127, 5), "Test case part2 failed"

    ans2 = find_contiguous_sum(numbers, ans1, 25)
    print(f"Answer part 2: {ans2}")
