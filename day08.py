#!/Users/geert/opt/anaconda3/bin/python3
from computer import Computer

def flip_instruction(ins):
    if ins[0] == "jmp":
        ins[0] = "nop"
    elif ins[0] == "nop":
        ins[0] = "jmp"

if __name__=="__main__":    
    
    test_program = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    ct = Computer()
    ct.load_instructions(test_program)
    error, acc = ct.run()
    assert 5 == acc, "Failed test case"
    
    from aoc_utils import load_text
    c = Computer()
    c.load_instructions(load_text("input/d08_pt1.txt"))
    error, acc = c.run()
    
    ## Part 2
    ct.instructions[-2][0] = "nop"
    ct.reset()
    error, acc = ct.run()
    assert 8 == acc, "Failed test case 2"
    
    # Oh boy... try to switch all jmp to nop and nop to jmp and see if it works..
    for i in range(len(c.instructions)):
        # flip jmp/nop
        flip_instruction(c.instructions[i])
        c.reset()
        error, acc = c.run()
        if error == 0:
            print(f"Got it! Changed instruction {i} to {c.instructions[i]}; acc is {acc}")
            break
        # flip back
        flip_instruction(c.instructions[i])