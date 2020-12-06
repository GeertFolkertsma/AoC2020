#!/Users/geert/opt/anaconda3/bin/python3

def count_unique_answers_for_group(g):
    return len(set(g.replace("\n","")))

def count_all_answers_for_group(g):
    # for group g, find which answer was given by all
    answers = list(map(set,g.split("\n")))
    all_given = answers[0].intersection(*answers)
    return len(all_given)

if __name__ == "__main__":
    testinput = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    import re
    testgroups = re.split("\n\n", testinput)
    assert 11 == sum(map(count_unique_answers_for_group,testgroups)), "test case 1 failed"
    
    from aoc_utils import load_list
    groups = load_list("input/d06_pt1.txt","\n\n")
    # print(groups)
    
    ans1 = sum(map(count_unique_answers_for_group, groups))
    print(f"Answer part 1: {ans1}")
    
    ## Part 2
    assert 6 == sum(map(count_all_answers_for_group, testgroups)), "test case 2 failed"
    
    ans2 = sum(map(count_all_answers_for_group, groups))
    print(f"Answer part 2: {ans2}")