#/usr/bin/env python3

import random

class IntPuter:
    def __init__(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0
        self.rbp = 0
        self.waiting_for_input = False
        self.halted = False
    
    def reset(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0
        self.rbp = 0
        self.waiting_for_input = False
        self.halted = False
    
    def needs_input(self):
        return self.waiting_for_input
    
    def give_input(self, ii):
        self.i.append(ii)
        if self.waiting_for_input:
            self.waiting_for_input = False
            
    def has_output(self):
        return len(self.o) > 0
    
    def output(self):
        res = self.o[0]
        self.o = self.o[1:]
        return res
    
    def is_halted(self):
        return self.halted

    def _value(self, val, mode):
        if mode == 0:   # from mem
            if val >= len(self.m):
                return 0
            elif val < 0:
                raise Exception("Negative address read")
            else:
                return self.m[val]
        elif mode == 2: # relative
            if val+self.rbp >= len(self.m):
                return 0
            elif val+self.rbp < 0:
                raise Exception("Negative address read (relative mode)")
            else:
                return self.m[val+self.rbp]
        else:           # immediate
            return val
    
    def _set_value(self, adr, mode, val):
        if mode == 0:
            if adr >= len(self.m):
                self.m = self.m + ([0]*(adr-len(self.m))) + [val]
            elif adr < 0:
                raise Exception("Negative address write")                
            else:
                self.m[adr] = val
        elif mode == 2:
            if adr+self.rbp >= len(self.m):
                self.m = self.m + ([0]*(adr+self.rbp-len(self.m))) + [val]
            elif adr+self.rbp < 0:
                raise Exception("Negative address write (relative mode)")
            else:
                self.m[adr+self.rbp] = val
        else:
            raise Exception("Illegal mode for writing")

    def step(self):
        if self.halted or self.waiting_for_input:
            return False
        
        instruction = self.m[self.pc]
        ui = instruction % 100 # Micro instruction
        instruction = instruction // 100
        ms = [] # Modes
        for i in range(4):
            ms.append(instruction%10)
            instruction = instruction // 10
        
        if ui == 1:     # add
            v1 = self._value(self.m[self.pc+1], ms[0])
            v2 = self._value(self.m[self.pc+2], ms[1])

            self._set_value(self.m[self.pc+3], ms[2], v1 + v2)
            
            self.pc += 4
        elif ui == 2:   # mul
            v1 = self._value(self.m[self.pc+1], ms[0])
            v2 = self._value(self.m[self.pc+2], ms[1])

            self._set_value(self.m[self.pc+3], ms[2], v1 * v2)
            
            self.pc += 4
        elif ui == 3:   # in
            if len(self.i) == 0:
                self.waiting_for_input = True
                return False

            self._set_value(self.m[self.pc+1], ms[0], self.i[0])
            self.i = self.i[1:]
            
            self.pc += 2
        elif ui == 4:   # out
            self.o.append(self._value(self.m[self.pc+1], ms[0]))
            
            self.pc += 2
        elif ui == 5:   # jnz
            if self._value(self.m[self.pc+1], ms[0]) != 0:
                self.pc = self._value(self.m[self.pc+2], ms[1])
            else:
                self.pc += 3
        elif ui == 6:   # jz
            if self._value(self.m[self.pc+1], ms[0]) == 0:
                self.pc = self._value(self.m[self.pc+2], ms[1])
            else:
                self.pc += 3
        elif ui == 7:   # jlt
            if self._value(self.m[self.pc+1], ms[0]) < self._value(self.m[self.pc+2], ms[1]):
                self._set_value(self.m[self.pc+3], ms[2], 1)
            else:
                self._set_value(self.m[self.pc+3], ms[2], 0)
                
            self.pc += 4
        elif ui == 8:   # jeq
            if self._value(self.m[self.pc+1], ms[0]) == self._value(self.m[self.pc+2], ms[1]):
                self._set_value(self.m[self.pc+3], ms[2], 1)
            else:
                self._set_value(self.m[self.pc+3], ms[2], 0)
            self.pc += 4
        elif ui == 9:   # srbp
            self.rbp += self._value(self.m[self.pc+1], ms[0])
            self.pc += 2
        elif ui == 99:  # halt
            self.pc += 1
            self.halted = True

            return False
        else:
            raise Exception("Unexpected instruction %s encountered as position %s" % (self.m[self.pc], self.pc))
        
        return True

    def run(self):
        while self.step():
            pass

memory = []
while True:
    try:
        line = input()

        if line == "":
            break

        for m in line.split(","):
            memory.append(int(m))

    except ValueError:
        break
    except EOFError:
        break
    
def next_location(d, l):
    if d == 1:
        return (l[0], l[1]-1)
    elif d == 2:
        return (l[0], l[1]+1)
    elif d == 3:
        return (l[0]-1, l[1])
    elif d == 4:
        return (l[0]+1, l[1])
    else:
        raise Exception("Unexpected direction %s" % (d))

def possible_moves(l):
    res = []
    for d in range(4):
        res.append(next_location(d+1, l))
    return res

# Phase 1 - determine the map

cpu = IntPuter(memory, [])
direction = 1
location = (0, 0)
walls = []
visited = []
to_visit = [(0, -1), (0, 1), (-1, 0), (1, 0)]
goal = (-100, -100)
i = 0
while not cpu.is_halted() and len(to_visit) > 0:
    if location not in visited:
        visited.append(location)
        
    # Is there an unknown neighbour? Then visit
    next_dir = -1
    for d in range(4):
        if next_location(d+1, location) in to_visit:
            next_dir = d+1
            break
    
    # If no unknown neighbour, randomly walk around
    while next_dir == -1:
        d = random.randint(1, 4)
        if next_location(d, location) not in walls:
            next_dir = d
            break
        
    direction = next_dir
        
    # Execute IntPuter
    cpu.give_input(direction)
    cpu.run()
    out = cpu.output()
    
    # We need to know what the next location would have been, if the move was succesful
    next_loc = next_location(direction, location)
    if next_loc in to_visit:
        to_visit.remove(next_loc)
    
    if out == 0: # wall
        # We hit a wall, not it
        if next_loc not in walls:
            walls.append(next_loc)
        
    elif out == 1: # move
        location = next_loc
        
        for l in possible_moves(location):
            if l not in visited:
                if l not in to_visit:
                    to_visit.append(l)
    elif out == 2: # oxygen tank (and move)
        location = next_loc
        goal = location
        
        for l in possible_moves(location):
            if l not in visited:
                if l not in to_visit:
                    to_visit.append(l)
    else:
        raise Exception("Unexpected status")

def print_map(walls, visited, goal):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    for l in walls:
        if l[0] < minx:
            minx = l[0]
        if l[0] > maxx:
            maxx = l[0]
        if l[1] < miny:
            miny = l[1]
        if l[1] > maxy:
            maxy = l[1]
            
    for l in visited:
        if l[0] < minx:
            minx = l[0]
        if l[0] > maxx:
            maxx = l[0]
        if l[1] < miny:
            miny = l[1]
        if l[1] > maxy:
            maxy = l[1]

    for yi in range(maxy-miny+1):
        l = ""
        for xi in range(maxx-minx+1):
            x = xi + minx
            y = maxy - yi
            
            c = "."
            if (x,y) in walls:
                c = "#"
            if (x,y) in visited:
                c = " "
            if (x,y) == (0,0):
                c = "+"
            if (x,y) == goal:
                c = "X"
            l = l+c

        print(l)

print_map(walls, visited, goal)
    
# Phase 2 - walk the labyrinth
# A.k.a. recursion in Python sucks

distances = {}
distances[(0,0)] = 0

to_visit = visited.copy()

# This most likely does not always generate an optimal map, e.g. it does not 
# update the distance if encountering a non-optimal path. It works for my input, though
while len(to_visit) > 0:
    for nl in to_visit:
        min_distance = -1
        for n in possible_moves(nl):
            if n in distances:
                if min_distance == -1 or min_distance > distances[n]:
                    min_distance = distances[n]
        if min_distance != -1:
            distances[nl] = min_distance + 1
            to_visit.remove(nl)
            break
    
print("a: %s" % (distances[goal]))

goal_distances = {}
goal_distances[goal] = 0

to_visit = visited.copy()

# This most likely does not always generate an optimal map, e.g. it does not 
# update the distance if encountering a non-optimal path. It works for my input, though
while len(to_visit) > 0:
    for nl in to_visit:
        min_distance = -1
        for n in possible_moves(nl):
            if n in goal_distances:
                if min_distance == -1 or min_distance > goal_distances[n]:
                    min_distance = goal_distances[n]
        if min_distance != -1:
            goal_distances[nl] = min_distance + 1
            to_visit.remove(nl)
            break

print("b: %s" % (max(goal_distances.values())))
