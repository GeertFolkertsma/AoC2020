#!/Users/geert/opt/anaconda3/bin/python3

def extract_input(lines):
    # l is the list of inputs
    state = "rules"
    mine = []
    others = []
    rules = {}
    for l in lines:
        if l == "":
            state = "looking"
            continue
        if state == "rules":
            key, r = l.split(": ")
            rules[key] = []
            for rr in r.split(" or "):
                rrr = list(map(int,rr.split("-")))
                rules[key] += list(range(rrr[0],rrr[1]+1))
        elif state == "looking":
            if l == "your ticket:":
                state = "mine"
                continue
            elif l == "nearby tickets:":
                state = "others"
                continue
        elif state == "mine":
            mine = [*map(int,l.split(","))]
        elif state == "others":
            others.append([*map(int,l.split(","))])
    return rules,mine,others,

def sum_invalid_fields(rules, tickets):
    # return the sum of all fields that do not fit in any of the rules
    all_valid_numbers = set(inner for outer in rules.values() for inner in outer)
    invalid_sum = sum(val for ticket in tickets for val in ticket if val not in all_valid_numbers)
    return invalid_sum

def validate_ticket(all_valid_numbers, ticket):
    return all(val in all_valid_numbers for val in ticket)

if __name__ == "__main__":
    from aoc_utils import load_list
    testinput = load_list("input/d16_test.txt")
    
    rules, mine, others = extract_input(testinput)
    assert 71 == sum_invalid_fields(rules, others), "Test case pt1 failed"
    
    rules, mine, others = extract_input(load_list("input/d16_pt1.txt"))
    ans1 = sum_invalid_fields(rules, others)
    print(f"Answer pt1: {ans1}")
    
    # Pt 2: first discard invalid tickets
    all_valid_numbers = set(inner for outer in rules.values() for inner in outer)
    valid_tickets = [ticket for ticket in others if validate_ticket(all_valid_numbers, ticket)]
    assert len(valid_tickets) < len(others), "No tickets were invalidated"
    
    # now look for candidates for each key
    candidate_fields = {key: [i for i in range(len(valid_tickets[0])) if all(ticket[i] in rules[key] for ticket in valid_tickets)] for key in rules}
    
    field_keys = {}
    for i in range(len(candidate_fields)):
        fields = [field for field in candidate_fields if len(candidate_fields[field])==1]
        if len(fields) == 0:
            raise ValueException("No solvable field left :(")
        field = fields[0]
        val = candidate_fields[field][0]
        field_keys[field] = val
        for f in candidate_fields:
            if val in candidate_fields[f]:
                candidate_fields[f].remove(val)
    print(field_keys)
    assert len(field_keys) == len(rules), "Not all fields identified!"
    
    from functools import reduce
    from operator import mul
    
    ans2 = reduce(mul, (mine[field_keys[f]] for f in field_keys if f.startswith("departure")), 1)
    print(f"Answer part 2: {ans2}")
    