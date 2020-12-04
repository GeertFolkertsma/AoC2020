#!/Users/geert/opt/anaconda3/bin/python3

def load_passports(fn=None,text=None):
    import re
    if text is None:
        data = re.split("\n\n", load_text(fn))
    else:
        data = re.split("\n\n", text)
    passports = []
    for pdata in data:
        passport = {}
        for keyval in pdata.split():
            k,v = keyval.split(":")
            passport[k] = v
        passports.append(passport)
    return passports
    
def check_validity(passport, required_fields):
    return all(k in passport for k in required_fields)

def check_validity2(passport, required_fields):
    if not check_validity(passport, required_fields):
        return False
    if len(passport["byr"]) != 4:
        return False
    if not (1920 <= int(passport["byr"]) <= 2002):
        return False
    if len(passport["iyr"]) != 4:
        return False
    if not (2010 <= int(passport["iyr"]) <= 2020):
        return False
    if len(passport["eyr"]) != 4:
        return False
    if not (2020 <= int(passport["eyr"]) <= 2030):
        return False
    if passport["hgt"][-2:] == "cm":
        if not (150 <= int(passport["hgt"][:-2]) <= 193):
            return False
    elif passport["hgt"][-2:] == "in":
        if not (59 <= int(passport["hgt"][:-2]) <= 76):
            return False
    else:
        return False
    import re
    if not re.match(r'^#[0-9a-f]{6}$', passport["hcl"]):
        return False
    if passport["ecl"] not in ["amb","blu","brn","gry","grn","hzl","oth"]:
        return False
    if not re.match(r'^[0-9]{9}$', passport["pid"]):
        return False
    return True

if __name__ == "__main__":
    from aoc_utils import load_text
    
    required_fields = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]
    optional_fields = ["cid"]
    
    test_passports = load_passports("input/d04_test.txt")
    print(test_passports)
    
    from aoc_utils import count_valid
    def part1_validator(passport):
        return check_validity(passport, required_fields)
    
    test_valid = count_valid(test_passports, part1_validator)
    print(f"Test case 1 valid: {test_valid}")
    assert test_valid == 2, "test case part 1 failed"
    
    passports = load_passports("input/d04_pt1.txt")
    pt1_valid = count_valid(passports, part1_validator)
    print(f"Part 1 answer: {pt1_valid}")
    
    ### PART 2
    def part2_validator(passport):
        return check_validity2(passport, required_fields)
    
    invalid_passports = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    assert count_valid(load_passports(text=invalid_passports), part2_validator) == 0, "invalid test failed"
    
    valid_passports = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
    assert count_valid(load_passports(text=valid_passports), part2_validator) == 4, "valid passports failed"
    
    pt2_valid = count_valid(passports, part2_validator)
    print(f"Part 2 answer: {pt2_valid}")