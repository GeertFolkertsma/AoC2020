#!/Users/geert/opt/anaconda3/bin/python3


def count_trees(chart, slope, start=(0,0)):
    # chart is a list of strings
    # x and 0 start at 0 and increase right/down (x/y)
    dx = slope[0]
    dy = slope[1]
    
    x0 = start[0]
    y0 = start[1]
    Y = len(chart)
    X = len(chart[0])
    s = 0
    x = x0
    for y in range(y0,Y,dy):
        # print(x,y,chart[y][x % X])
        s += (chart[y][x % X] == "#")
        x += dx
    return s

def generate_chart_counter(chart):
    def chart_counter(slope):
        return count_trees(chart, slope)
    return chart_counter

if __name__=="__main__":
    from aoc_utils import load_list
    
    test_check = 7
    test_data = load_list("input/d03_test.txt")
    # print(test_data)
    
    test_ans = count_trees(test_data, (3,1))
    assert test_ans == test_check, "test case 1 failed"
    
    data = load_list("input/d03_p1.txt")
    ans1 = count_trees(data, (3,1))
    print(f"Answer to part 1: {ans1}")
    
    ## Part 2
    slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    
    test_counts_check = [2,7,3,4,2]
    test_prod = 336
    
    test_chart_counter = generate_chart_counter(test_data)
    test_counts = list(map(test_chart_counter, slopes))
    # print(*test_counts)
    assert all(c == test_counts_check[i] for i,c in enumerate(test_counts)), "test case 2 failed"
    # calculate product
    from functools import reduce
    from operator import mul
    
    prod_test = reduce(mul, test_counts, 1)
    print(f"Test product: {prod_test}")
    assert prod_test == test_prod, "test case 2.2 failed"
    
    chart_counter = generate_chart_counter(data)
    prod = reduce(mul, map(chart_counter, slopes) , 1)
    print(f"Answer part 2: {prod}")