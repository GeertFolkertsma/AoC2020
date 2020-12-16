#!/Users/geert/opt/anaconda3/bin/python3

def take_n_turns(start_sequence, n=2020):
    sequence = start_sequence.copy()
    seen_at = {n: [t] for t,n in enumerate(sequence)}
    for t in range(len(sequence),n):
        # determine next number
        # find whether we had seen last number before
        last_number = sequence[-1]
        if last_number in seen_at and len(seen_at[last_number]) > 1:
            n = seen_at[last_number][-1] - seen_at[last_number][-2]
        else:
            n = 0
        if n not in seen_at:
            seen_at[n] = []
        seen_at[n].append(t)
        sequence.append(n)
    # print(sequence)
    return sequence[-1]

if __name__ == "__main__":
    
    testcases = [([0,3,6],436,175594),([1,3,2],1,2578),([2,1,3],10,3544142),([1,2,3],27,261214),([2,3,1],78,6895259),([3,2,1],438,18),([3,1,2],1836,362)]
    
    # take_n_turns(testcases[0][0],10)
    
    for test in testcases:
        assert take_n_turns(test[0]) == test[1], f"Test case pt 1 {test} failed"
    
    # actually do pt 1
    real_sequence = [19,0,5,1,10,13]
    ans1 = take_n_turns(real_sequence)
    print(f"Answer to part 1: {ans1}")
    
    t_end = 30000000
    # take_n_turns(testcases[0][0],t_end)
    ans2 = take_n_turns(real_sequence,n=t_end)
    print(f"Answer to part 2: {ans2}")