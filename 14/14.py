#/usr/bin/env python3

import math

def from_ore(amount, substance, rules, spares):
    # Try to use spares first
    if substance in spares:
        if spares[substance] >= amount:
            spares[substance] = spares[substance] - amount
            print("TAKE %s %s from spares" % (amount, substance))
            return 0
        else:
            print("TAKE %s %s from spares, %s left" % (spares[substance], substance, amount-spares[substance]))
            amount -= spares[substance] 
            del spares[substance]

    # Look at what rule to use to get the substance
    rule = rules[substance]
    
    # Calculate how many times to apply the rule
    multiplier = math.ceil(amount / rule[0])

    # Holds the amount of ore used
    res = 0
    # Iterate over all inputs
    for r in rule[1]:
        print("%s %s => %s %s" % (r[1]*multiplier, r[0], amount, substance))
        
        if r[0] == 'ORE':
            # If we are dealing with ore, simple 
            res += r[1]*multiplier
        else:
            res += from_ore(r[1]*multiplier, r[0], rules, spares)
            
        if rule[0]*multiplier > amount:
            print("SAVE %s %s" % (rule[0]*multiplier - amount, substance))
            if substance in spares:
                spares[substance] = spares[substance] + rule[0]*multiplier - amount
            else:
                spares[substance] = rule[0]*multiplier - amount

    return res

assert from_ore(1, 'FUEL', {'A':   (10, [('ORE', 10)]),
                            'B':   (1,  [('ORE', 1)]),
                            'C':   (1,  [('A', 7), ('B', 1)]),
                            'D':   (1,  [('A', 7), ('C', 1)]),
                            'E':   (1,  [('A', 7), ('D', 1)]),
                            'FUEL':(1,  [('A', 7), ('E', 1)])}, {}) == 31

print("---")

assert from_ore(1, 'FUEL', {'A':   (2, [('ORE', 9)]),
                            'B':   (3, [('ORE', 8)]),
                            'C':   (5, [('ORE', 7)]),
                            'AB':  (1, [('A', 3), ('B', 4)]),
                            'BC':  (1, [('B', 5), ('C', 7)]),
                            'CA':  (1, [('C', 4), ('A', 1)]),
                            'FUEL':(1, [('AB', 2), ('BC', 3), ('CA', 4)])}, {}) == 165

print("---")

import re

def rule_fragment_from_line(f):
    m = re.match("^\s*(\d+)\s+(\w+)\s*$", f)
    return (m.group(2), int(m.group(1)))

def add_line_to_rules(l, rules):
    sides = l.split("=>")
    out = rule_fragment_from_line(sides[1])
    ins = []
    for f in sides[0].split(","):
        ins.append(rule_fragment_from_line(f))
    rules[out[0]] = (out[1], ins)

rules = {}
add_line_to_rules("10 ORE => 10 A", rules)
add_line_to_rules("1 ORE => 1 B", rules)
add_line_to_rules("7 A, 1 B => 1 C", rules)
add_line_to_rules("7 A, 1 C => 1 D", rules)
add_line_to_rules("7 A, 1 D => 1 E", rules)
add_line_to_rules("7 A, 1 E => 1 FUEL", rules)
assert from_ore(1, 'FUEL', rules, {}) == 31
print("---")

rules = {}
add_line_to_rules("9 ORE => 2 A", rules)
add_line_to_rules("8 ORE => 3 B", rules)
add_line_to_rules("7 ORE => 5 C", rules)
add_line_to_rules("3 A, 4 B => 1 AB", rules)
add_line_to_rules("5 B, 7 C => 1 BC", rules)
add_line_to_rules("4 C, 1 A => 1 CA", rules)
add_line_to_rules("2 AB, 3 BC, 4 CA => 1 FUEL", rules)
assert from_ore(1, 'FUEL', rules, {}) == 165
print("---")

rules = {}
add_line_to_rules("44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL", rules)
assert rules['FUEL'] == (1, [('XJWVT', 44), ('KHKGT', 5), ('QDVJ', 1), ('NZVS', 29), ('GPVTF', 9), ('HKGWZ', 48)])

add_line_to_rules("157 ORE => 5 NZVS", rules)
add_line_to_rules("165 ORE => 6 DCFZ", rules)
add_line_to_rules("12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", rules)
add_line_to_rules("179 ORE => 7 PSHF", rules)
add_line_to_rules("177 ORE => 5 HKGWZ", rules)
add_line_to_rules("7 DCFZ, 7 PSHF => 2 XJWVT", rules)
add_line_to_rules("165 ORE => 2 GPVTF", rules)
add_line_to_rules("3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT", rules)

assert from_ore(1, 'FUEL', rules, {}) == 13312
print("---")

rules = {}
add_line_to_rules("2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG", rules)
add_line_to_rules("17 NVRVD, 3 JNWZP => 8 VPVL", rules)
add_line_to_rules("53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL", rules)
add_line_to_rules("22 VJHF, 37 MNCFX => 5 FWMGM", rules)
add_line_to_rules("139 ORE => 4 NVRVD", rules)
add_line_to_rules("144 ORE => 7 JNWZP", rules)
add_line_to_rules("5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC", rules)
add_line_to_rules("5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV", rules)
add_line_to_rules("145 ORE => 6 MNCFX", rules)
add_line_to_rules("1 NVRVD => 8 CXFTF", rules)
add_line_to_rules("1 VJHF, 6 MNCFX => 4 RFSQX", rules)
add_line_to_rules("176 ORE => 6 VJHF", rules)

print(from_ore(1, 'FUEL', rules, {}))
print("---")
assert from_ore(1, 'FUEL', rules, {}) == 180697
print("---")

rules = {}
add_line_to_rules("171 ORE => 8 CNZTR", rules)
add_line_to_rules("7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL", rules)
add_line_to_rules("114 ORE => 4 BHXH", rules)
add_line_to_rules("14 VRPVC => 6 BMBT", rules)
add_line_to_rules("6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL", rules)
add_line_to_rules("6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT", rules)
add_line_to_rules("15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW", rules)
add_line_to_rules("13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", rules)
add_line_to_rules("5 BMBT => 4 WPTQ", rules)
add_line_to_rules("189 ORE => 9 KTJDG", rules)
add_line_to_rules("1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", rules)
add_line_to_rules("12 VRPVC, 27 CNZTR => 2 XDBXC", rules)
add_line_to_rules("15 KTJDG, 12 BHXH => 5 XCVML", rules)
add_line_to_rules("3 BHXH, 2 VRPVC => 7 MZWV", rules)
add_line_to_rules("121 ORE => 7 VRPVC", rules)
add_line_to_rules("7 XCVML => 6 RJRHP", rules)
add_line_to_rules("5 BHXH, 4 VRPVC => 5 LTCX", rules)

print(from_ore(1, 'FUEL', rules, {}))
print("---")
assert from_ore(1, 'FUEL', rules, {}) == 2210736
print("---")

exit()

rules = {}
while True:
    try:
        line = input()
        add_line_to_rules(line, rules)
    except ValueError:
        break
    except EOFError:
        break

print("a: %s" % (from_ore(1, 'FUEL', rules, {}))) # 156344 is too low
