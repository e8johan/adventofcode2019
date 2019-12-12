#/usr/bin/env python3

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

hull = {}
d = (0, -1)
l = (0, 0)
hull[l] = 1
cpu = IntPuter(memory, [])
while not cpu.is_halted():
    cpu.run()
    if cpu.needs_input():
        if l in hull:
            cpu.give_input(hull[l])
        else:
            cpu.give_input(0)
        cpu.run()
    if cpu.has_output():
        hull[l] = cpu.output() # Colour
        if cpu.output() == 0:
            # left
            d = (d[1], -d[0])
        else:
            # right
            d = (-d[1], d[0])
        l = (l[0] + d[0], l[1] + d[1])

minx = 0
maxx = 0
miny = 0
maxy = 0
for l in hull.keys():
    x = l[0]
    y = l[1]
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y

assert minx == 0
assert miny == 0

def print_rows(rows):
    for r in rows:
        l = ""
        for c in r:
            l += c
        print(l)

rows = []
for y in range(maxy+1):
    rows.append(['.']*(maxx+1))

for l in hull.keys():
    x = l[0]
    y = l[1]

    if hull[l] == 1:
        rows[y][x] = "#"

print_rows(rows)
