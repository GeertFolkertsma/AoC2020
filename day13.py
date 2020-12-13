#!/Users/geert/opt/anaconda3/bin/python3



testinput = """939
7,13,x,x,59,x,31,19"""

if __name__ == "__main__":
    t0, buses = testinput.split()
    t0 = int(t0)
    buses = [int(b) for b in buses.split(",") if b != "x"]
    
    # print(t0,buses)
    
    # Part 1 is simple: b - t % b is the remaining wait time
    tw = [b - (t0 % b) for b in buses]
    minT = min(tw)
    minB = buses[tw.index(minT)]
    assert minT*minB == 295, "test part 1 failed"
    
    from aoc_utils import load_list
    t0, buses_txt = load_list("input/d13_pt1_laura.txt")
    t0 = int(t0)
    buses = [int(b) for b in buses_txt.split(",") if b != "x"]
    tw = [b - (t0 % b) for b in buses]
    minT = min(tw)
    minB = buses[tw.index(minT)]
    print(minT, minB)
    ans1 = minT * minB
    print(f"Answer to part 1: {ans1}")
    
    # Part 2 is hard! modulo and MMI is not fun
    from aoc_utils import prime_factors
    # print(prime_factors(1068781+4))
    
    t0_min = 100000000000000
    
    to_find = buses.copy()
    
    bus_to_offset = {b: buses_txt.split(",").index(str(b)) for b in buses}
    print(to_find, bus_to_offset)
    
    inc = 1
    t = t0_min
    searching = True
    while searching:
        t += inc
        for b in to_find:
            if (t + bus_to_offset[b]) % b == 0:
                inc *= b
                to_find.remove(b)
                print(f"Found {b} at t={t}; to_find={to_find}")
                if len(to_find) == 0:
                    t_start = t# - bus_to_offset[b]
                    searching = False
                break
    #1028248271342300 is not right
    print(f"t_start = {t_start}")
    # verify answer:
    for b in buses:
        t = t_start + bus_to_offset[b]
        print(f"t = {t}; offset={bus_to_offset[b]} t (mod b) = {t%b}")