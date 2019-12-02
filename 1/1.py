#/usr/bin/env python3

from math import floor

def fuel_for_mass_a(mass):
    return (mass//3)-2

assert(fuel_for_mass_a(12) == 2)
assert(fuel_for_mass_a(14) == 2)
assert(fuel_for_mass_a(1969) == 654)
assert(fuel_for_mass_a(100756) == 33583)

def fuel_for_mass_b(fuel):
    res = 0
    ff = fuel
    while True:
        ff = fuel_for_mass_a(ff)
        if ff > 0:
            res += ff
        else:
            return res

assert(fuel_for_mass_b(14) == 2)
assert(fuel_for_mass_b(1969) == 966)
assert(fuel_for_mass_b(100756) == 50346)

needed_fuel_a = 0
needed_fuel_b = 0

while True:
    try:
        mass = int(input())
    except ValueError:
        break
    except EOFError:
        break

    needed_fuel_a += fuel_for_mass_a(mass)
    needed_fuel_b += fuel_for_mass_b(mass)

print("Needed fuel (a): %s" % (needed_fuel_a))
print("Needed fuel (b): %s" % (needed_fuel_b))
