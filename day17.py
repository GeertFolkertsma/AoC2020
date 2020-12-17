#!/Users/geert/opt/anaconda3/bin/python3
import operator

def init_conway(l,dims=3):
    # l is list of initial state
    active = []
    z = 0
    if dims == 4:
        w = 0
    for y,r in enumerate(l):
        for x,c in enumerate(r):
            if c == "#":
                if dims == 3:
                    active.append((x,y,z))
                elif dims == 4:
                    active.append((x,y,z,w))
                else:
                    raise NotImplementedError("Only 3D or 4D allowed.")
    return active

def step_conway(cells):
    mins, maxs = get_minmaxs(cells)
    new_cells = []
    for x in range(mins[0]-1,maxs[0]+2):
        for y in range(mins[1]-1,maxs[1]+2):
            for z in range(mins[2]-1,maxs[2]+2):
                # we try to decide next x,y,z
                n = count_neighbours((x,y,z), cells)
                # print(f"Check for {(x,y,z)} => {n}")
                if (x,y,z) in cells:
                    if n in [2,3]:
                        new_cells.append((x,y,z))
                elif n==3:
                    new_cells.append((x,y,z))
    return new_cells

def step_conway4(cells):
    mins, maxs = get_minmaxs(cells,dims=4)
    # print(mins, maxs)
    new_cells = []
    for x in range(mins[0]-1,maxs[0]+2):
        for y in range(mins[1]-1,maxs[1]+2):
            for z in range(mins[2]-1,maxs[2]+2):
                for w in range(mins[3]-1,maxs[3]+2):
                    # we try to decide next x,y,z,w
                    n = count_neighbours((x,y,z,w), cells, dims=4)
                    # print(f"Check for {(x,y,z,w)} => {n}")
                    if (x,y,z,w) in cells:
                        if n in [2,3]:
                            new_cells.append((x,y,z,w))
                    elif n==3:
                        new_cells.append((x,y,z,w))
    return new_cells

def count_neighbours(p, cells, dims=3):
    # count all neighbours of the cells
    count = sum(1 for c in cells if all(abs(c[i]-p[i])<2 for i in range(dims)))
    if p in cells:
        count -= 1
    return count

def get_minmaxs(cells,dims=3):
    mins = [min(cells, key=operator.itemgetter(i))[i] for i in range(dims)]
    maxs = [max(cells, key=operator.itemgetter(i))[i] for i in range(dims)]
    return mins, maxs

def print_conway(cells):
    mins, maxs = get_minmaxs(cells)
    # now print all layers
    for z in range(mins[2],maxs[2]+1):
        print(f"\nz={z}")
        for y in range(mins[1],maxs[1]+1):
            s = ""
            for x in range(mins[0],maxs[0]+1):
                if (x,y,z) in cells:
                    s += "#"
                else:
                    s += "."
            print(s)

if __name__ == "__main__":
    from aoc_utils import load_list
    
    test_input = """.#.
..#
###""".splitlines()
    testcells = init_conway(test_input)
    print_conway(testcells)
    
    # cells = step_conway(testcells)
    # print_conway(cells)
    
    cells = testcells.copy()
    for i in range(6):
        cells = step_conway(cells)
    assert 112 == len(cells), "Test case part 1 failed"
    
    realcells = init_conway(load_list("input/d17_pt1.txt"))
    
    cells = realcells.copy()
    for i in range(6):
        cells = step_conway(cells)
    ans1 = len(cells)
    print(f"Answer part 1: {ans1}")
    
    testcells4d = init_conway(test_input,dims=4)
    # print(testcells4d)
    for i in range(6):
        testcells4d = step_conway4(testcells4d)
    assert 848 == len(testcells4d), "Test case pt2 failed"
    
    realscells4d = init_conway(load_list("input/d17_pt1.txt"),dims=4)
    for i in range(6):
        realscells4d = step_conway4(realscells4d)
    ans2 = len(realscells4d)
    print(f"Answer part 2: {ans2}")