#!/Users/geert/opt/anaconda3/bin/python3

import regex as re

orientations = "NESW"

mirror_orientation = {"N": "S", "E": "W", "S": "N", "W": "E"}

flip_and_dir_to_edges = {}
flip_and_dir_to_edges[(False, "N")] = ("T","R","B","L")
flip_and_dir_to_edges[(False, "E")] = ("Lr","T","Rr","B")
flip_and_dir_to_edges[(False, "S")] = ("Br","Lr","Tr","Rr")
flip_and_dir_to_edges[(False, "W")] = ("R","Br","L","Tr")
flip_and_dir_to_edges[(True, "N")] = ("Tr","L","Br","R")
flip_and_dir_to_edges[(True, "E")] = ("Rr","Tr","Lr","Br")
flip_and_dir_to_edges[(True, "S")] = ("B","Rr","T","Lr")
flip_and_dir_to_edges[(True, "W")] = ("L","B","R","T")



class Tile:
    orientations = "NESW"
    sides = "TRBL"
    
    def __init__(self, number, txt):
        self.number = number
        self.txt = txt
        self.txt_orig = txt
        self.orientation = "N" # where does the T point now
        self.flipud = False
        self.calculate_edges()
        self.calculate_current_edges()
        self.to_match = [o for o in self.orientations]
        
    
    def calculate_edges(self):
        self.all_edges = {} # original TRDL, TiRiDiLi
        txt_arr = self.txt_orig.replace("#","1").replace(".","0").splitlines()
        self.all_edges["T"] = int(txt_arr[0],2)
        self.all_edges["Tr"] = int(txt_arr[0][::-1],2)
        self.all_edges["B"] = int(txt_arr[-1],2)
        self.all_edges["Br"] = int(txt_arr[-1][::-1],2)
        self.all_edges["R"] = int("".join(r[-1] for r in txt_arr),2)
        self.all_edges["Rr"] = int("".join(r[-1] for r in txt_arr[::-1]),2)
        self.all_edges["L"] = int("".join(r[0] for r in txt_arr),2)
        self.all_edges["Lr"] = int("".join(r[0] for r in txt_arr[::-1]),2)
    
    def calculate_current_edges(self):
        self.current_edges = {} # current NESW
        self.selected_edges = {}
        # self.orientation {N,E,S,W} tells where the Top is pointing now
        sides = flip_and_dir_to_edges[(self.flipud, self.orientation)]
        for i in range(4):
            self.current_edges[self.orientations[i]] = self.all_edges[sides[i]]
            self.selected_edges[self.orientations[i]] = sides[i]
    
    def calculate_orientation(self, relative_location, s):
        # Calculate our required orientation if we are <relative_location> of someone and need <s> as an edge value there
        # relative_location is where we are w.r.t. the neighbour
        # s is the required edge's num
        required_edge = [o for o in self.all_edges if self.all_edges[o]==s][0]
        my_edge = mirror_orientation[relative_location]
        flip_and_o = [k for k in flip_and_dir_to_edges if flip_and_dir_to_edges[k][self.orientations.index(my_edge)] == required_edge][0]
        # print(relative_location, required_edge, flip_and_o)
        self.flipud, self.orientation = flip_and_o
        self.calculate_current_edges()
        # print(flip_and_o)
    
    def get_actual_lines(self):
        # Given the current orientation and fliplr, return 8x8 text
        lines = []
        txt_arr = self.txt_orig.splitlines()
        for outy in range(1,9):
            lines.append([])
            for outx in range(1,9):
                x = outx
                y = outy
                for i in range(self.orientations.index(self.orientation)):
                    x, y = y, 9-x
                if self.flipud:
                    x = 9 - x
                lines[outy-1].append(txt_arr[y][x])
        return lines

def generate_tiles(txt):
    tiles_txt = txt.split("\n\n")
    tiles = {}
    for tile_txt in tiles_txt:
        idtxt, t = tile_txt.split(":\n")
        tileid = int(idtxt[-4:])
        tile = Tile(tileid, t)
        tiles[tileid] = tile
        # print(tile.selected_edges,tile.current_edges)
    # Get all IDs
    return tiles

def match_tiles(tiles):
    all_sides = sorted(sum([list(tiles[tileid].all_edges.values()) for tileid in tiles],[]))
    # print(all_sides)
    not_ok = []
    for s in all_sides:
        if all_sides.count(s) > 2:
            not_ok.append(s)
    assert len(not_ok)==0, "More than one solution!"
    
    suggested_orientations = {}
    for s in all_sides:
        if all_sides.count(s) == 2:
            # try to find the two matching tiles
            matching_tiles = [tilenum for tilenum in tiles if s in tiles[tilenum].all_edges.values()]
            # print(f"For {s}: matching tiles are {matching_tiles}")
            for tilenum in matching_tiles:
                orientation = [k for k in tiles[tilenum].all_edges if tiles[tilenum].all_edges[k] == s]
                # print(f"Suggested orientation for {tilenum} is {orientation}")
                if tilenum not in suggested_orientations:
                    suggested_orientations[tilenum] = orientation
                else:
                    suggested_orientations[tilenum] += orientation
    # print(suggested_orientations)
    match_counts = {k: len(suggested_orientations[k]) for k in suggested_orientations}
    # print(match_counts)
    corners = [k for k in match_counts if match_counts[k] == 8]
    return corners

def make_puzzle(tiles, start_tilenum):
    # all possible orientations are possible
    # start tile has set orientation
    in_puzzle = {start_tilenum: (0,0)}
    to_lay = list(tiles.keys())
    to_lay.remove(start_tilenum)
    while len(to_lay) > 0:
        to_match = {tileid: tiles[tileid].to_match for tileid in in_puzzle if len(tiles[tileid].to_match)>0}
        for fixed_tileid in to_match:
            for edge in to_match[fixed_tileid]:
                s = tiles[fixed_tileid].current_edges[edge]
                # print(f"Looking for {fixed_tileid} {edge}: {s}")
                for candidate_id in to_lay:
                    if s in tiles[candidate_id].all_edges.values():
                        # now find which edge of candidate_id we should have
                        t = tiles[candidate_id]
                        t.calculate_orientation(edge, s)
                        # hooray, now add that to in_puzzle, and remove these two edges
                        t.to_match.remove(mirror_orientation[edge])
                        # print(f"Matched {candidate_id}")
                        x,y = in_puzzle[fixed_tileid]
                        if edge == "N":
                            y -= 1
                        elif edge == "S":
                            y += 1
                        elif edge == "E":
                            x += 1
                        elif edge == "W":
                            x -= 1
                        to_lay.remove(candidate_id)
                        in_puzzle[candidate_id] = (x,y)
                # now it has been matched, or is an edge piece
                tiles[fixed_tileid].to_match.remove(edge)
    # print(to_lay,in_puzzle)
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    loc_to_tileid = {}
    for tileid in in_puzzle:
        minx = min(minx, in_puzzle[tileid][0])
        maxx = max(maxx, in_puzzle[tileid][0])
        miny = min(miny, in_puzzle[tileid][1])
        maxy = max(maxy, in_puzzle[tileid][1])
        loc_to_tileid[in_puzzle[tileid]] = tileid
    # print(f"Puzzle goes from ({minx},{miny}) to ({maxx},{maxy})")
    
    # Now lay the puzzle :o
    puzzle = []
    pieces = ""
    for y in range(miny, maxy+1):
        for i in range(8):
            puzzle.append([])
        for x in range(minx, maxx+1):
            t = tiles[loc_to_tileid[(x,y)]]
            pieces += f"\t{t.number}"
            # print(t.number)
            lines = t.get_actual_lines()
            for i in range(8):
                puzzle[8*(y-miny)+i] += lines[i]
        pieces += "\n"
    
    # generate single string from puzzle
    puzzle_txt = ""
    for line in puzzle:
        puzzle_txt += "".join(line) + "\n"
    print(pieces)
    print(puzzle_txt)
    return puzzle_txt

def count_monsters(puzzle_text):
    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()
    # print(monster)
     
    puzzle_width = len(puzzle_text.splitlines()[0])
    monster_width = len(monster[0])
    # print(puzzle_width, monster_width)
    monster_text = (" "*(puzzle_width - monster_width)).join(monster)
    
    monster_regex = monster_text.replace(" ",".")
    puzzle_string = puzzle_text.replace("\n","")
    
    prog = re.compile(monster_regex)
    print(prog)
    # print(puzzle_string)
    # print(prog.match(puzzle_string))
    return len(prog.findall(puzzle_string, overlapped=True)), monster_text

if __name__ == "__main__":
    from aoc_utils import load_text
    
    testtiles = generate_tiles(load_text("input/d20_test.txt"))
    
    corners = match_tiles(testtiles)
    
    from functools import reduce
    from operator import mul
    
    test_corner_mult = reduce(mul, corners, 1)
    assert 20899048083289 == test_corner_mult, "Test case part 1 failed"
    
    
    realtiles = generate_tiles(load_text("input/d20_pt1.txt"))
    corners = match_tiles(realtiles)
    ans1 = reduce(mul, corners, 1)
    print(f"Answer part 1: {ans1}")
    
    # Part 2
    # TEST
    # for flip in [True, False]:
    #     for o in "NESW":
    #         testtiles = generate_tiles(load_text("input/d20_test.txt"))
    #         master_tile = testtiles[1951]
    #         master_tile.flipud = flip
    #         master_tile.orientation = o
    #         master_tile.calculate_current_edges()
    #         print(flip,o)
    #         # for l in master_tile.get_actual_lines():
    #             # print("".join(l))
    #         # print("\n".join(master_tile.get_actual_lines()))
    #         puzzle_text = make_puzzle(testtiles,1951)
    #         # print(flip,o,count_monsters(puzzle_text))
    #         n_monsters, monster_text = count_monsters(puzzle_text)
    #         if n_monsters > 0:
    #             sea_roughness = puzzle_text.count("#") - n_monsters * monster_text.count("#")
    #             assert 273 == sea_roughness

    for flip in [True]:
        for o in "E":
            realtiles = generate_tiles(load_text("input/d20_pt1.txt"))
            master_tile = realtiles[2609]
            master_tile.flipud = flip
            master_tile.orientation = o
            master_tile.calculate_current_edges()
            print(flip,o)
            # for l in master_tile.get_actual_lines():
                # print("".join(l))
            # print("\n".join(master_tile.get_actual_lines()))
            puzzle_text = make_puzzle(realtiles,2609)
            # print(flip,o,count_monsters(puzzle_text))
            n_monsters, monster_text = count_monsters(puzzle_text)
            if n_monsters > 0:
                sea_roughness = puzzle_text.count("#") - (n_monsters) * monster_text.count("#")
                ans2 = sea_roughness
                print(f"Found monsters: {n_monsters}")
    print(f"Answer to part 2: {ans2}")