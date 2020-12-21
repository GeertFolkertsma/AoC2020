#!/Users/geert/opt/anaconda3/bin/python3

def parse_foods(foodlist):
    all_ingredients = []
    all_allergens = []
    allergens_to_ingredients = {}
    for food in foodlist:
        ingredients, allergens = food[:-1].split(" (contains ")
        ingredients = ingredients.split(" ")
        allergens = allergens.split(", ")
        all_ingredients += ingredients
        for allergen in allergens:
            if allergen in allergens_to_ingredients:
                allergens_to_ingredients[allergen] = allergens_to_ingredients[allergen].intersection(set(ingredients))
            else:
                allergens_to_ingredients[allergen] = set(ingredients)
        # print(allergens_to_ingredients)
    return all_ingredients, all_allergens, allergens_to_ingredients

def get_canonical_list(foodlist):
    _, _, atoi = parse_foods(foodlist)
    # atoi is allergens to ingredient, hehe
    # print(atoi)
    itoa = {} # ingredient to allergen, duh
    while True:
        one_option = [k for k in atoi if len(atoi[k])==1]
        if len(one_option) < 1:
            break
        a = one_option[0]
        i = next(iter(atoi[a]))# next/iter just takes the one option
        itoa[i] = a 
        for k in atoi:
            if i in atoi[k]:
                atoi[k].remove(i)
        atoi.pop(a)
        # print(atoi)
    return ",".join(sorted(list(itoa.keys()), key=lambda i: itoa[i]))

def count_safe_ingredients(foodlist):
    all_ingredients, all_allergens, allergens_to_ingredients = parse_foods(foodlist)
    
    # print(allergens_to_ingredients)
    possibly_unsafe_ingredients = set()
    for ingredients in allergens_to_ingredients.values():
        possibly_unsafe_ingredients |= ingredients
    # print(possibly_unsafe_ingredients)
    
    return len(all_ingredients) - sum(all_ingredients.count(ingredient) for ingredient in possibly_unsafe_ingredients)

if __name__ == "__main__":
    from aoc_utils import load_list
    
    testcase = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines()
    
    assert 5 == count_safe_ingredients(testcase), "Test case part 1 failed"
    
    real_foodlist = load_list("input/d21_pt1.txt")
    
    ans1 = count_safe_ingredients(real_foodlist)
    print(f"Answer to part 1: {ans1}")
    
    # Part 2: figure out which is which
    assert "mxmxvkd,sqjhc,fvjkl" == get_canonical_list(testcase), "Test case part 2 failed"
    
    ans2 = get_canonical_list(real_foodlist)
    print(f"Answer to part 2: {ans2}")
    