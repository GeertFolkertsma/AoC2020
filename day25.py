#!/Users/geert/opt/anaconda3/bin/python3


def find_exp(public_key, base, modulo):
    key = 1
    exp = 0
    while key != public_key:
        exp += 1
        key = pow(base, exp, modulo)
    return exp

def calc_encryption_key(public_keys, exponents, modulo):
    secret1 = pow(public_keys[0], exponents[1], modulo)
    secret2 = pow(public_keys[1], exponents[0], modulo)
    assert secret1 == secret2, "Different encryption keys found"
    return secret1

if __name__ == "__main__":
    modulo = 20201227
    base = 7
    
    test_pubs = [5764801, 17807724]
    
    secrets = [find_exp(pub, base, modulo) for pub in test_pubs]
    assert secrets == [8,11], "Test case: wrong exponents found"
    
    assert 14897079 == calc_encryption_key(test_pubs, secrets, modulo), "Test case: wrong encryption key found"
    
    
    real_pubs = [14082811,5249543]
    secrets = [find_exp(pub, base, modulo) for pub in real_pubs]
    ans1 = calc_encryption_key(real_pubs, secrets, modulo)
    print(f"Answer to part 1: {ans1}")