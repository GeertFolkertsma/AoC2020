#!/Users/geert/opt/anaconda3/bin/python3
import re

child_re = re.compile(r'(\d+) (.+) bags?')

def parse_rule(r):
    # <x> bags contain <n1> <y1> bag(s), <n2> <y2> bag(s). OR no other bags
    parent, children = r.split(" bags contain ")
    if children == "no other bags.":
        return parent, None
    children = children.split(',')
    c_dict = {}
    for child in children:
        match = child_re.search(child)
        c_dict[match.group(2)] = int(match.group(1))
    return parent, c_dict

def make_rule_dicts(rules):
    c_to_p_ = {} # c_to_p will represent a directed graph or linked list child -> parent
    # c_to_p['child'] = ['parent1','parent2', ....]
    p_to_c_ = {} # directed graph parent to child
    # p_to_c['parent'] = {'child1': n1, 'child2': n2}
    for r in (rules):
        parent, children = parse_rule(r)
        if children is None:
            continue
        p_to_c_[parent] = children
        for c in children:
            if c not in c_to_p_:
                c_to_p_[c] = []
            c_to_p_[c].append(parent)
    return p_to_c_, c_to_p_

def count_parents(child):
    # c_to_p has a list of all parents that can carry child
    # there might be branches in there, though, so have to count unique holder only
    parents = get_all_parents(child)
    return len(parents)

def get_all_parents(child):
    if child not in c_to_p:
        # we're not held by anyone
        return set()
    # print(set(c_to_p[child]))
    s = set(c_to_p[child])
    for p in c_to_p[child]:
        # print(get_all_parents(p))
        s |= get_all_parents(p)
    return s

def count_children(parent):
    if parent not in p_to_c:
        return 0
    s = 0
    for child in p_to_c[parent]:
        n = p_to_c[parent][child]
        s += n + n * count_children(child)
    return s

if __name__ == "__main__":
    from aoc_utils import load_list
    testrules = load_list("input/d07_test.txt")
    # print(testrules)
    
    p_to_c, c_to_p = make_rule_dicts(testrules)
    # print(p_to_c)
    # print(c_to_p)
    # print(get_all_parents("shiny gold"))
    print(count_parents("shiny gold"))
    assert 4 == count_parents("shiny gold"), "num parents test failed"
    
    rules = load_list("input/d07_pt1.txt")
    
    p_to_c, c_to_p = make_rule_dicts(rules)
    
    ans1 = count_parents("shiny gold")
    print(f"Answer part 1: {ans1}")
    
    ## Part 2
    p_to_c, c_to_p = make_rule_dicts(testrules)
    assert 32 == count_children("shiny gold"), "test case part 2 failed"
    
    p_to_c, c_to_p = make_rule_dicts(rules)
    ans2 = count_children("shiny gold")
    print(f"Answer part 2: {ans2}")