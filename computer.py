

class Computer:
    def __init__(self, debug=False):
        self.acc = 0
        self.pointer = 0
        self.instructions = []
        self._debug = debug
    
    def load_instructions(self, ins):
        self.instructions = [i.split() for i in ins.splitlines()]
        self.reset()
    
    def reset(self):
        self.acc = 0
        self.pointer = 0
        self.executed_list = []
    
    def run(self):
        while self.pointer not in self.executed_list:
            new_pointer = self.step(self.pointer)
            self.executed_list.append(self.pointer)
            if new_pointer == len(self.instructions):
                if self._debug:
                    print(f"Finished execution normally: would go to {self.pointer}; acc is {self.acc}")
                return 0, self.acc
            self.pointer = new_pointer
        if self._debug:
            print(f"Finished execution with error: would go to {self.pointer}; acc is now {self.acc}")
        return 1, self.acc
    
    def step(self, pointer):
        ins = self.instructions[pointer]
        if self._debug:
            print(ins)
        # big switch/case
        if ins[0] == "nop":
            pointer += 1
        elif ins[0] == "acc":
            self.acc += int(ins[1])
            pointer += 1
        elif ins[0] == "jmp":
            pointer += int(ins[1])
        else:
            print("Error: invalid instruction {ins}")
        
        return pointer