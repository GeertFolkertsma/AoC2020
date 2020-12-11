#!/Users/geert/opt/anaconda3/bin/python3
import copy

def step_conway(floor):
    newfloor = copy.deepcopy(floor)
    Y = len(floor)
    X = len(floor[0])
    changed = False
    for y,r in enumerate(floor):
        for x,c in enumerate(r):
            if c == ".":
                continue
            neighbours = 0
            xmin = max(0,x-1)
            xmax = min(x+1,X-1)
            ymin = max(0,y-1)
            ymax = min(y+1,Y-1)
            for y_ in range(ymin,ymax+1):
                for x_ in range(xmin,xmax+1):
                    # print(f"x={x},y={y},(x_,y_)={x_},{y_}; {xmin}-{xmax}")
                    if floor[y_][x_] == '#' and (x,y) != (x_,y_):
                        neighbours += 1
            if neighbours == 0:
                newfloor[y][x] = '#'
                if floor[y][x] != '#':
                    changed = True
            elif neighbours >= 4:
                newfloor[y][x] = 'L'
                if floor[y][x] != 'L':
                    changed = True
    return newfloor, changed

def step_conway2(floor):
    newfloor = copy.deepcopy(floor)
    Y = len(floor)
    X = len(floor[0])
    changed = False
    for y,r in enumerate(floor):
        for x,c in enumerate(r):
            if c == ".":
                continue
            neighbours = 0
            for direction in [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                neighbours += find_neighbour(floor, x, y, direction[0], direction[1])
            if neighbours == 0:
                newfloor[y][x] = '#'
                if floor[y][x] != '#':
                    changed = True
            elif neighbours >= 5:
                newfloor[y][x] = 'L'
                if floor[y][x] != 'L':
                    changed = True
    return newfloor, changed

def find_neighbour(floor, x, y, dx, dy):
    Y = len(floor)
    X = len(floor[0])
    x_ = x + dx
    y_ = y + dy
    while (x_ >= 0 and x_ < X) and (y_ >= 0 and y_ < Y):
        if floor[y_][x_] == '#':
            return 1
        elif floor[y_][x_] == 'L':
            return 0
        x_ += dx
        y_ += dy
    return 0

def print_conway(floor):
    for r in floor:
        print("".join(r))
    print("\n\n")

def floors_same(floora, floorb):
    for y,r in enumerate(floora):
        for x,c in enumerate(r):
            if c != floorb[y][x]:
                # print(f"{c} != {floorb[y][x]}, x={x},y={y}")
                return False
    return True

def run_until_convergence(floor, fn=step_conway):
    i = 0
    while True:
        i += 1
        newfloor, changed = fn(floor)
        if not changed:#floors_same(newfloor, floor):
            print(f"Convergence reached after {i} steps")
            return newfloor
        floor = newfloor

def count_occupied(floor):
    return sum(r.count('#') for r in floor)

if __name__ == "__main__":
    test_data = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    testfloor = list(map(list,test_data.split()))
    
    final = run_until_convergence(testfloor)
    print_conway(final)
    assert count_occupied(final) == 37, "Test part 1 failed"
    
    from aoc_utils import load_text
    realfloor = list(map(list,load_text("input/d11_pt1.txt").split()))
    # print_conway(realfloor)
    
    # final = run_until_convergence(realfloor)
    # ans1 = count_occupied(final)
    # print(f"Answer part 1: {ans1}")
    
    final = run_until_convergence(testfloor,fn=step_conway2)
    print_conway(final)
    assert 26 == count_occupied(final), "Test part 2 failed"
    
    final = run_until_convergence(realfloor,fn=step_conway2)
    ans2 = count_occupied(final)
    print(f"Answer part 2: {ans2}")