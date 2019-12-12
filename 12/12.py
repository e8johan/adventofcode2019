#/usr/bin/env python3

import re

class Planet:
    def __init__(self, x, y, z):
        self.posx = x
        self.posy = y
        self.posz = z
        
        self.kinx = 0
        self.kiny = 0
        self.kinz = 0
        
        self.nextx = 0
        self.nexty = 0
        self.nextz = 0
        
    def calc_gravity(self, x, y, z):
        if self.posx < x:
            self.nextx += 1
        elif self.posx > x:
            self.nextx -= 1
        
        if self.posy < y:
            self.nexty += 1
        elif self.posy > y:
            self.nexty -= 1

        if self.posz < z:
            self.nextz += 1
        elif self.posz > z:
            self.nextz -= 1
    
    def apply_gravity(self):
        self.kinx += self.nextx
        self.kiny += self.nexty
        self.kinz += self.nextz
        
        self.posx += self.kinx
        self.posy += self.kiny
        self.posz += self.kinz

        self.nextx = 0
        self.nexty = 0
        self.nextz = 0

    def energy(self):
        return (abs(self.posx) + abs(self.posy) + abs(self.posz)) * (abs(self.kinx) + abs(self.kiny) + abs(self.kinz))
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "Planet(pos: <" + str(self.posx) + ", " + str(self.posy) + ", " + str(self.posz) + ">, kin: <" + str(self.kinx) + ", " + str(self.kiny) + ", " + str(self.kinz) + ">)"

def step(planets):
    for p in planets:
        for q in planets:
            p.calc_gravity(q.posx, q.posy, q.posz)
    for p in planets:
        p.apply_gravity()
        
def energy_sum(planets):
    res = 0
    for p in planets:
        res += p.energy()
    return res

def planet_system(planets):
    return ((planets[0].posx, planets[1].posx, planets[2].posx, planets[3].posx, planets[0].kinx, planets[1].kinx, planets[2].kinx, planets[3].kinx), 
            (planets[0].posy, planets[1].posy, planets[2].posy, planets[3].posy, planets[0].kiny, planets[1].kiny, planets[2].kiny, planets[3].kiny), 
            (planets[0].posz, planets[1].posz, planets[2].posz, planets[3].posz, planets[0].kinz, planets[1].kinz, planets[2].kinz, planets[3].kinz))

def gdc(a, b):
    while b:
        t = b
        b = a % b
        a = t

    return a

def lcm(a, b):
    return a*b // gdc(a, b)

def find_cycle(planets):
    initial = planet_system(planets)
    
    cycles = [0]*3
    i = 0
    while True:
        step(planets)
        i += 1
        
        state = planet_system(planets)
        found = True
        for a in range(3):
            if cycles[a] == 0:
                if state[a] == initial[a]:
                    cycles[a] = i
                else:
                    found = False
        
        if found:
            break
        
    return lcm(cycles[0], lcm(cycles[1], cycles[2]))

planets = [Planet(-1, 0, 2), Planet(2, -10, -7), Planet(4, -8, 8), Planet(3, 5, -1)]
step(planets)
assert planets[0].posx == 2
assert planets[0].posy == -1
assert planets[0].posz == 1
assert planets[0].kinx == 3
assert planets[0].kiny == -1
assert planets[0].kinz == -1
assert planets[1].posx == 3
assert planets[1].posy == -7
assert planets[1].posz == -4
assert planets[2].posx == 1
assert planets[2].posy == -7
assert planets[2].posz == 5
step(planets)
assert planets[0].posx == 5
assert planets[0].posy == -3
assert planets[0].posz == -1
assert planets[0].kinx == 3
assert planets[0].kiny == -2
assert planets[0].kinz == -2
step(planets)
step(planets)
step(planets)
assert planets[0].posx == -1
assert planets[0].posy == -9
assert planets[0].posz == 2
assert planets[0].kinx == -3
assert planets[0].kiny == -1
assert planets[0].kinz == 2
for i in range(5):
    step(planets)
assert planets[0].energy() == 36
assert planets[1].energy() == 45
assert planets[2].energy() == 80
assert planets[3].energy() == 18
assert energy_sum(planets) == 179

assert find_cycle([Planet(-1, 0, 2), Planet(2, -10, -7), Planet(4, -8, 8), Planet(3, 5, -1)]) == 2772
assert find_cycle([Planet(-8, -10, 0), Planet(5, 5, 10), Planet(2, -7, 3), Planet(9, -8, -3)]) == 4686774924

pa = []
pb = []
while True:
    try:
        line = input()

        if line == "":
            break
        
        m = re.match("^<x=(\-?\d+), y=(\-?\d+), z=(\-?\d+)>$", line)
        pa.append(Planet(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        pb.append(Planet(int(m.group(1)), int(m.group(2)), int(m.group(3))))

    except ValueError:
        break
    except EOFError:
        break

for i in range(1000):
    step(pa)
print("a: %s" % (energy_sum(pa)))
print("b: %s" % (find_cycle(pb)))
