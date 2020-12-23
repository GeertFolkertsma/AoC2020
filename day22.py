#!/Users/geert/opt/anaconda3/bin/python3
from collections import deque

def get_decks(text):
    decks = []
    for p in text.split("\n\n"):
        decks.append(list(map(int,p.split("\n")[1:])))
    return decks

class Combat:
    def __init__(self, decks):
        self.decks = list(map(deque, decks))
        # print(self.decks)
    
    def play_round(self):
        cards = [d.popleft() for d in self.decks]
        winner = cards[1] > cards[0]
        self.decks[winner].append(cards[winner])
        self.decks[winner].append(cards[~winner])
        # print(self.decks)
    
    def calculate_score(self, deck=None):
        if deck is None:
            # assume game was ended; take the largest deck
            deck = max(self.decks,key=len)
        N = len(deck)
        score = sum((N-i)*c for i,c in enumerate(deck))
        return score
        
    def play_classic(self):
        while all(len(d) for d in self.decks) > 0:
            self.play_round()
        # now determine the score
        return self.calculate_score()
    
    def play_round_recursive(self):
        cards = [d.popleft() for d in self.decks]
        if all(len(self.decks[i]) >= c for i,c in enumerate(cards)):
            # recurse, to beat that cocky crab
            newdecks = [list(self.decks[i])[:c] for i,c in enumerate(cards)]
            # print(f"Playing recursive game with {newdecks}")
            childgame = Combat(newdecks)
            winner, score = childgame.play_recursive()
        else:
            winner = cards[1] > cards[0]
        self.decks[winner].append(cards[winner])
        self.decks[winner].append(cards[~winner])
        # print(self.decks)
    
    def play_recursive(self):
        self.history = []
        while all(len(d) for d in self.decks) > 0:
            self.play_round_recursive()
            decks = tuple(map(tuple,self.decks))
            if decks in self.history:
                # win by recursion: player 1 --> 0
                return (0, self.calculate_score(self.decks[0]))
            self.history.append(decks)
        if len(self.decks[0]) > 0:
            return 0, self.calculate_score(self.decks[0])
        else:
            return 1, self.calculate_score(self.decks[1])

if __name__ == "__main__":
    from aoc_utils import load_text
    
    testcase1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    
    testgame = Combat(get_decks(testcase1))
    assert 306 == testgame.play_classic(), "Test part 1 failed"
    
    realgame = Combat(get_decks(load_text("input/d22_pt1.txt")))
    ans1 = realgame.play_classic()
    print(f"Answer part 1: {ans1}")
    
    testcase2 = """Player 1:
43
19

Player 2:
2
29
14"""
    testgame2 = Combat(get_decks(testcase2))
    w2, _ = testgame2.play_recursive()
    assert w2 == 0, "Player 1 repetition game not won"
    
    testgame3 = Combat(get_decks(testcase1))
    winner, score = testgame3.play_recursive()
    assert 291 == score, "Recursive test case failed"
    
    realgame_recursive = Combat(get_decks(load_text("input/d22_pt1.txt")))
    _, ans2 = realgame_recursive.play_recursive()
    print(f"Answer part 2: {ans2}")