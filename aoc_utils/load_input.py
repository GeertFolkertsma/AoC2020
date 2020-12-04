#!/Users/geert/opt/anaconda3/bin/python3
def load_text(fn):
    with open(fn) as f:
        return f.read()

def load_list(fn):
    return load_text(fn).split("\n")

def load_ints(fn):
    return list(map(int, load_list(fn)))

if __name__ == "__main__":
    import os
    sample_input_file = os.path.join(os.path.dirname(__file__),"../input/d1_test.txt")
    
    data = load_list(sample_input_file)
    print(f"{data!r}")
    
    data = load_ints(sample_input_file)
    print(f"{data!r}")