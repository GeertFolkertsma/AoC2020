#!/Users/geert/opt/anaconda3/bin/python3

def parse_row(s):
    # convert string (first 7 bits) to int
    # B is high bit, F is low bit
    s = s[:7].replace("B","1").replace("F","0")
    return int(s,2)

def parse_column(s):
    # convert last 3 bits to seat number
    # R is high bit, L is low bit
    s = s[7:].replace("L","0").replace("R","1")
    return int(s,2)

def get_seat_id(s):
    # seat id is row * 8 + column
    return int(s.replace("B","1").replace("F","0").replace("L","0").replace("R","1"),2)

if __name__ == "__main__":
    testseat = "FBFBBFFRLR"
    assert parse_row(testseat) == 44, "rowtest failed"
    assert parse_column(testseat) == 5, "columntest failed"
    assert get_seat_id(testseat) == 357, "seat test failed"
    
    assert get_seat_id("BFFFBBFRRR") == 567, "test2 failed"
    assert get_seat_id("FFFBBBFRRR") == 119, "test3 failed"
    assert get_seat_id("BBFFBBFRLL") == 820, "test4 failed"
    
    # Part 1: get highest seat id
    from aoc_utils import load_list
    passes = load_list("input/d05_pt1.txt")
    ans = max(map(get_seat_id,passes))
    print(f"Answer part 1: {ans}")
    
    # Part 2: get own seat that is a gap between two others
    all_seats = sorted(list(map(get_seat_id, passes)))
    for i,seat in enumerate(all_seats):
        if all_seats[i+1] - seat == 2:
            print(f"Seats {seat} and {all_seats[i+1]} occupied: my seat is {seat+1}")
            break
    