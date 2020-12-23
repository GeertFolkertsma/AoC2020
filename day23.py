#!/Users/geert/opt/anaconda3/bin/python3
from collections import deque

class CrabCups:
    def __init__(self, cups, extended=False):
        self.cups_orig = cups
        self.extended = extended
        self.reset()
    
    def reset(self):
        self.cups = deque(map(int,self.cups_orig))
        self.min_cup = min(self.cups)
        self.max_cup = max(self.cups)
        if self.extended:
            self.cups.extend(range(self.max_cup+1,1_000_001))
            self.max_cup = max(self.cups)
        self.L = len(self.cups)
    
    def move(self):
        # a. pick up the three cups CW of current cup
        current_cup = self.cups.popleft()
        pickup = [self.cups.popleft() for i in range(3)]
        d = current_cup - 1
        if d < self.min_cup:
            d = self.max_cup
        while d in pickup:
            d -= 1
            if d < self.min_cup:
                d = self.max_cup
        insert_idx = self.cups.index(d)
        # self.cups.rotate(-insert_idx-1)
        # self.cups.extendleft(pickup[::-1])
        # self.cups.rotate(insert_idx+1)
        if insert_idx == self.L:
            self.cups.extend(pickup)
        else:
            for c in pickup[::-1]:
                self.cups.insert(insert_idx+1, c)
        self.cups.appendleft(current_cup)
        self.cups.rotate(-1)
        
        # print(self.cups)
    
    def play_game(self, M=100):
        for m in range(M):
            self.move()
        # we have rotated -M times
        self.cups.rotate(M%self.L)
        # and now we must move 1 to the front
        self.cups.rotate(-self.cups.index(1))
        self.cups.popleft()
        if self.extended:
            return [self.cups.popleft() for i in range(2)]
        else:
            return "".join(map(str,self.cups))

class Cup:
    def __init__(self, val):
        self.val = val
        self.next = None
    def linknext(self, c):
        # link ourselves to left of the c (link on the right to c)
        # ie c becomes next
        self.next = c
    def __str__(self):
        return str(self.val)
    def __repr__(self):
        return f"{self.val} -> {self.next}"
    
class CrabCupsLL:
    def __init__(self, cups, extended=False):
        self.cups_init = cups
        self.extended = extended
        print(cups)
        self.reset()
    
    def reset(self):
        self.N = 1_000_000 if self.extended else len(self.cups_init)
        self.cups = {}
        for i in range(1,self.N+1):
            self.cups[i] = Cup(i)
        # set up the links
        cups_order = list(map(int, self.cups_init))
        if self.extended:
            cups_order += list(range(len(self.cups_init)+1, self.N+1))
        for i,c in enumerate(cups_order):
            self.cups[cups_order[i-1]].linknext(self.cups[c])
        self.current = self.cups[cups_order[0]]
        # print(self.cups)
        # print(self.cups[cups_order[-1]].__repr__())
        print(f"Current: {self.current!r}")
        
    def move(self):
        # current cup is self.cups[self.current] (or self.current, indeed)
        # we want to pick up the next three
        pickup = self.current.next
        insert_at = self.current.val - 1
        if insert_at < 1:
            insert_at = self.N
        pickup_vals = [pickup.val, pickup.next.val, pickup.next.next.val]
        while insert_at in pickup_vals:
            insert_at -= 1
            if insert_at < 1:
                insert_at = self.N
        # now insert those three cups after that cup
        last_pickup = pickup.next.next
        # current next has to be the old next of the last pickup
        self.current.next = last_pickup.next
        # insert_at has to have its next set to first pickup, and last pickup's next should be insert_at's next
        insert_at = self.cups[insert_at]
        insert_at.next, last_pickup.next = pickup, insert_at.next
        # move on to the next cup
        self.current = self.current.next
    
    def play_game(self, T=100):
        self.reset()
        for t in range(T):
            self.move()
    
    def get_one_neighbours(self, N=2):
        nb = []
        current = self.cups[1]
        for n in range(N):
            current = current.next
            nb.append(current.val)
        # print(nb)
        return nb

if __name__ == "__main__":
    # from aoc_utils import load_text
    
    testcase1 = "389125467"
    
    testgame = CrabCups(testcase1)
    assert "92658374" == testgame.play_game(10), "Test game 10 moves failed"
    
    testgame.reset()
    assert "67384529" == testgame.play_game(100), "Test game 100 moves failed"
    
    realgame = CrabCups("364297581")
    ans1 = realgame.play_game(100)
    print(f"Answer part 1: {ans1}")
    
    # Part 2...
    realgame.extended = True
    realgame.reset()
    # import time
    # t0 = time.perf_counter()
    # print(realgame.play_game(1000))
    # t1 = time.perf_counter()
    # t_each = (t1-t0)/1000
    # t_tenmillion = 10e6 * t_each
    # print(f"Time for 1000: {t1-t0:.1f}; for 10e6: {t_tenmillion:.0f}")
    
    # TOO SLOW!!
    
    testgame2 = CrabCupsLL(testcase1,False)
    testgame2.play_game(100)
    assert "67384529" == "".join(map(str,testgame2.get_one_neighbours(8)))
    
    realgame2 = CrabCupsLL("364297581",False)
    realgame2.play_game(100)
    ans1b = "".join(map(str,realgame2.get_one_neighbours(8)))
    print(f"Answer part 1, bis: {ans1b}")
    
    # part 2, again
    realgame2 = CrabCupsLL("364297581",True)
    realgame2.play_game(10_000_000)
    ans2 = realgame2.get_one_neighbours(2)
    print(ans2)
    ans2 = ans2[0] * ans2[1]
    print(f"Answer to part 2: {ans2}")