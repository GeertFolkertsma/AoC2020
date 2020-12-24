#!/Users/geert/opt/anaconda3/bin/python3

def get_black_cells(txt):
    txt = txt.replace("ne","a").replace("se","b").replace("sw","c").replace("nw","d")
    dirs = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "w": 0}
    black_cells = set()
    for l in txt.splitlines():
        for d in dirs:
            dirs[d] = l.count(d)
        cell = (2*dirs["e"]+dirs["a"]+dirs["b"] - 2*dirs["w"]-dirs["c"]-dirs["d"],2*(dirs["a"]+dirs["d"]-dirs["b"]-dirs["c"]))
        if cell in black_cells:
            black_cells.remove(cell)
        else:
            black_cells.add(cell)
    return black_cells


def get_neighbours(black_cells, cell):
    # cell is a tuple (x,y)
    # black_cells is a set of tuples
    n = 0
    white_neighbours = set()
    for ofs in ((2,0),(-2,0),(-1,2),(1,2),(-1,-2),(1,-2)):
        neighbour = (cell[0]+ofs[0],cell[1]+ofs[1])
        # print(cell,neighbour,neighbour in black_cells)
        if neighbour in black_cells:
            n += 1
        else:
            white_neighbours.add(neighbour)
    return n, white_neighbours

def step_conway(black_cells):
    newcells = set()
    white_check = set()
    for cell in black_cells:
        n, wn = get_neighbours(black_cells, cell)
        # print(cell,n)
        if n in (1,2):
            newcells.add(cell)
        white_check |= wn
    for cell in white_check:
        n, _ = get_neighbours(black_cells, cell)
        if n == 2:
            newcells.add(cell)
    return newcells

if __name__ == "__main__":
    from aoc_utils import load_text
    
    assert 10 == len(get_black_cells(load_text("input/d24_test.txt"))), "Test case pt1 failed"
    
    ans1 = len(get_black_cells(load_text("input/d24_pt1.txt")))
    print(f"Answer to part 1: {ans1}")
    
    # Part 2
    cells = get_black_cells(load_text("input/d24_test.txt"))
    # print(cells)
    for i in range(100):
        cells = step_conway(cells)
    assert 2208 == len(cells), "Test case part 2 failed"
    
    cells = get_black_cells(load_text("input/d24_pt1.txt"))
    for i in range(100):
        cells = step_conway(cells)
    ans2 = len(cells)
    print(f"Answer to part 2: {ans2}")