#!/Users/geert/opt/anaconda3/bin/python3

class MyInt:
    def __init__(self, n):
        self.n = n
    def __mul__(self, o):
        return MyInt(self.n * o.n)
    def __add__(self, o):
        return MyInt(self.n + o.n)
    def __sub__(self, o):
        # make subtraction actually do multiplication
        return MyInt(self.n * o.n)
    def __truediv__(self, o):
        # make division actually do addition
        return MyInt(self.n + o.n)
    def __len__(self):
        return self.n

def calculate(s, part2=False):
    import re
    # First convert all ints to MyInts
    s = re.sub(r"(\d+)",r"MyInt(\1)",s)
    # Now we want * to be equal precendence to +, so use -
    s = s.replace("*","-")
    if part2:
        # addition must take precedence, so use / for that
        s = s.replace("+","/")
    return eval(f"len({s})")

if __name__ == "__main__":
    # test MYInt class
    i1 = MyInt(8)
    i2 = MyInt(5)
    assert 13 == len(i1+i2)
    assert 40 == len(i1*i2)
    assert 40 == len(i1 - i2)
    
    testcases = []
    testcases.append(("2 * 3 + (4 * 5)",26,46))
    testcases.append(("5 + (8 * 3 + 9 + 3 * 4 * 3)",437,1445))
    testcases.append(("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240,669060))
    testcases.append(("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632,23340))
    
    for t in testcases:
        assert t[1] == calculate(t[0]), f"Test case {t} failed"
    
    from aoc_utils import load_list
    homework = load_list("input/d18_pt1.txt")
    ans1 = sum(map(calculate, homework))
    print(f"Answer to part 1: {ans1}")
    
    # part 2: easy-peasy! just use truediv for +
    assert 13 == len(i1/i2)
    
    for t in testcases:
        assert t[2] == calculate(t[0],True), f"Test case {t} failed"
    
    ans2 = sum(map(lambda s: calculate(s,True), homework))
    print(f"Answer to part 2: {ans2}")