#!/Users/geert/opt/anaconda3/bin/python3

def parse_data(lines):
    # split the data into a tuple with (char,min,max,pw)
    # min-max<space>char:<space>password
    # regex probably slower than simple splitting
    output = []
    for line in lines:
        rule,pw = line.split(":")
        # pw has a leading space, but /care
        counts,char = rule.split(" ")
        m,M = map(int,counts.split("-"))
        output.append((char,m,M,pw))
    return output

def check_validity(t):
    # t is a tuple with (char,min,max,pw)
    return t[1] <= t[3].count(t[0]) <= t[2]

def check_validity2(t):
    # t is a tuple with (char,pos1,pos2,pw)
    # note: pos 1-indexed
    return ((t[3][t[1]] == t[0]) + (t[3][t[2]] == t[0])) == 1

if __name__ == "__main__":
    t1_data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".split("\n")
    t1_valid = 2
    
    parsed_pws_t = parse_data(t1_data)
    print(parsed_pws_t)
    assert sum(map(check_validity,parsed_pws_t)) == t1_valid, "test case 1 failed"
    
    from aoc_utils import load_list
    data = load_list("input/d02_p1.txt")
    
    parsed_pws = parse_data(data)
    ans = sum(map(check_validity,parsed_pws))
    print(f"Answer part 1: {ans}")
    
    ## Part 2
    assert sum(map(check_validity2,parsed_pws_t)) == 1, "test case 2 failed"
    
    ans2 = sum(map(check_validity2,parsed_pws))
    print(f"Answer part 2: {ans2}")