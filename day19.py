#!/Users/geert/opt/anaconda3/bin/python3
import re

def parse_rules(rules):
    rules_dict = {}
    for l in rules:
        k,r = l.split(": ")
        rules_dict[k] = r.strip('" ')
    master_rule = rules_dict["0"]
    find_digit = re.compile(r"(\d+)")
    match = find_digit.search(master_rule)
    while match:
        # print(master_rule)
        r = match.group(1)
        if r in ["8","11"]:
            print(r)
        master_rule = re.sub(r"\b"+r+r"\b",f"({rules_dict[r]})",master_rule)
        match = find_digit.search(master_rule)
    return "^" + master_rule.replace(" ","").replace("(a)","a").replace("(b)","b") + "$"

def parse_rules2(rules):
    rules_dict = {}
    for l in rules:
        k,r = l.split(": ")
        rules_dict[k] = "("+r.strip('" ')+")"
    master_rule = rules_dict["0"]
    rules_dict["8"] = "(42)+"
    rules_dict["11"] = r"(?P<PALINDROME>42 (?:(?P>PALINDROME)|.?) 31)"
    find_digit = re.compile(r"(\d+)")
    match = find_digit.search(master_rule)
    while match:
        # print(master_rule)
        r = match.group(1)
        master_rule = re.sub(r"\b"+r+r"\b",rules_dict[r],master_rule)
        match = find_digit.search(master_rule)
    return "^" + master_rule.replace(" ","").replace("(a)","a").replace("(b)","b") + "$"


if __name__ == "__main__":
    
    testrules1 = """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
""".splitlines()
    
    print(parse_rules(testrules1))
    
    testrules2, messages2 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".split("\n\n")
    regex_test2 = re.compile(parse_rules(testrules2.splitlines()))
    for m in messages2.splitlines():
        print(m,regex_test2.match(m))
    from aoc_utils import count_valid
    assert 2 == count_valid(messages2.splitlines(), regex_test2.match)

    from aoc_utils import load_text
    rules, messages = load_text("input/d19_pt1.txt").split("\n\n")
    regex = parse_rules(rules.splitlines())
    # print(regex)
    prog = re.compile(regex)
    ans1 = count_valid(messages.splitlines(), prog.match)
    print(f"Answer part 1: {ans1}")
    
    regex2 = parse_rules2(rules.splitlines())
    # print(regex2)
    import regex
    pattern = regex.compile(regex2)
    # print(pattern)
    
    testregex = r"(?P<PALINDROME>42 (?:(?P>PALINDROME)|\w?) 31)".replace(" ","")
    # testregex = r"(42(?:(?1)|(\w?))31)"
    testpattern = regex.compile(testregex)
    print(testpattern)
    print("match",testpattern.match("424242313131"))
    
    ans2 = count_valid(messages.splitlines(), pattern.match)
    print(f"Answer part 2: {ans2}")