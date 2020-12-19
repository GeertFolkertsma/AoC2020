
def count_valid(it,validator):
    return sum(1 for i in it if validator(i))