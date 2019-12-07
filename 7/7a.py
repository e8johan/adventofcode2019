#/usr/bin/env python3

class IntPuter:
    def __init__(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0
    
    def reset(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0

    def _value(self, val, mode):
        if mode == 0:   # from mem
            return self.m[val]
        else:           # immediate
            return val

    def step(self):
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

            self.m[self.m[self.pc+3]] = v1 + v2
            
            self.pc += 4
        elif ui == 2:   # mul
            v1 = self._value(self.m[self.pc+1], ms[0])
            v2 = self._value(self.m[self.pc+2], ms[1])

            self.m[self.m[self.pc+3]] = v1 * v2
            
            self.pc += 4
        elif ui == 3:   # in
            self.m[self.m[self.pc+1]] = self.i[0]
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
                self.m[self.m[self.pc+3]] = 1
            else:
                self.m[self.m[self.pc+3]] = 0
                
            self.pc += 4
        elif ui == 8:   # jeq
            if self._value(self.m[self.pc+1], ms[0]) == self._value(self.m[self.pc+2], ms[1]):
                self.m[self.m[self.pc+3]] = 1
            else:
                self.m[self.m[self.pc+3]] = 0
            self.pc += 4
        elif ui == 99:  # halt
            self.pc += 1

            return False
        else:
            raise Exception("Unexpected instruction %s encountered as position %s" % (self.m[self.pc], self.pc))
        
        return True

    def run(self):
        while self.step():
            pass
            

def thrust_from_phase(m, s):
    cpu = IntPuter(m, [s[0], 0])
    cpu.run()
    o = cpu.o[0]
    cpu.reset(m, [s[1], o])
    cpu.run()
    o = cpu.o[0]
    cpu.reset(m, [s[2], o])
    cpu.run()
    o = cpu.o[0]
    cpu.reset(m, [s[3], o])
    cpu.run()
    o = cpu.o[0]
    cpu.reset(m, [s[4], o])
    cpu.run()
    return cpu.o[0]

assert(thrust_from_phase([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4, 3, 2, 1, 0]) == 43210)
assert(thrust_from_phase([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321)
assert(thrust_from_phase([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210)

def find_max_thrust(m):
    res = 0
    for a in range(5):
        for b in filter(lambda x: x not in [a], range(5)):
            for c in filter(lambda x: x not in [a,b], range(5)):
                for d in filter(lambda x: x not in [a,b,c], range(5)):
                    for e in filter(lambda x: x not in [a,b,c,d], range(5)):
                        t = thrust_from_phase(m, [a,b,c,d,e])
                        if t > res:
                            res = t
    return res

assert(find_max_thrust([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210)
assert(find_max_thrust([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321)
assert(find_max_thrust([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210)

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

print("a: %s" % (find_max_thrust(memory)))
