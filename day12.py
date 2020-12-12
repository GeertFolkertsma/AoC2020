#!/Users/geert/opt/anaconda3/bin/python3
class Ship:
    dps = [(0,1),(1,0),(0,-1),(-1,0)]
    dirs = "NESW"
    
    def __init__(self, p0=None, dir_="E", wp0=None):
        if p0 is None:
            self.p = [0,0]
        else:
            self.p = p0
        self.d = self.dirs.index(dir_)
        
        self.wp = wp0
    
    def dir_to_dp(self, d):
        return self.dps[d]
    
    def rotate(self, d, deg):
        if d == "L":
            sign = -1
        else:
            sign = 1
        if self.wp is None:
            self.d += sign * int(deg/90)
            self.d %= 4
        else:
            n = int(sign * deg/90) % 4
            for i in range(n):
                # rotate CW, x := y; y := -x
                self.wp = [self.wp[1],-self.wp[0]]
    
    def forward(self, n):
        if self.wp is None:
            for i in range(2):
                self.p[i] += n * self.dps[self.d][i]
        else:
            for i in range(2):
                self.p[i] += n * self.wp[i]
    
    def move(self, d, n):
        if self.wp is not None:
            for i in range(2):
                self.wp[i] += n * self.dps[self.dirs.index(d)][i]
        else:
            for i in range(2):
                self.p[i] += n * self.dps[self.dirs.index(d)][i]
    
    def execute_step(self, s):
        a = s[:1]
        n = int(s[1:])
        if a in self.dirs:
            self.move(a,n)
        elif a in "LR":
            self.rotate(a, n)
        elif a == "F":
            self.forward(n)
        else:
            raise ValueError(f"Unknown instruction {s}")
    
    def get_manhattan_dist(self):
        return sum(map(abs,self.p))

if __name__ == "__main__":
    test_data = """F10
N3
F7
R90
F11"""

    test_route = test_data.split()
    
    testship = Ship()
    for s in test_route:
        testship.execute_step(s)
        # print(s,testship.p)
    assert 25 == testship.get_manhattan_dist(), "Test case pt1 failed"
    
    from aoc_utils import load_list
    route = load_list("input/d12_pt1.txt")
    ship = Ship(p0=[0,0])
    for s in route:
        ship.execute_step(s)
    ans1 = ship.get_manhattan_dist()
    print(f"Answer part 1: {ans1}")
    
    testship2 = Ship(wp0=[10,1])
    for s in test_route:
        testship2.execute_step(s)
        # print(s,testship2.p,testship2.wp)
    assert 286 == testship2.get_manhattan_dist(), "Test case pt2 failed"
    
    ship2 = Ship(wp0=[10,1])
    for s in route:
        ship2.execute_step(s)
    ans2 = ship2.get_manhattan_dist()
    print(f"Answer part 2: {ans2}")