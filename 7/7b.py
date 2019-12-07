#/usr/bin/env python3

class IntPuter:
    def __init__(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0
        self.waiting_for_input = False
        self.halted = False
    
    def reset(self, m, i):
        self.m = m.copy()
        self.i = i.copy()
        self.o = []
        self.pc = 0
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
            return self.m[val]
        else:           # immediate
            return val

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

            self.m[self.m[self.pc+3]] = v1 + v2
            
            self.pc += 4
        elif ui == 2:   # mul
            v1 = self._value(self.m[self.pc+1], ms[0])
            v2 = self._value(self.m[self.pc+2], ms[1])

            self.m[self.m[self.pc+3]] = v1 * v2
            
            self.pc += 4
        elif ui == 3:   # in
            if len(self.i) == 0:
                self.waiting_for_input = True
                return False

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
            self.halted = True

            return False
        else:
            raise Exception("Unexpected instruction %s encountered as position %s" % (self.m[self.pc], self.pc))
        
        return True

    def run(self):
        while self.step():
            pass
            

def thrust_from_phase(m, s):
    res = 0
    
    cpus = []
    for i in range(5):
        cpu = IntPuter(m, [s[i]])
        cpus.append(cpu)
        
    cpus[0].give_input(0)
    
    one_running = True
    while one_running:
        # Run all CPUs
        for c in cpus:
            c.run()
            
        # Propagate values
        for i in range(5):
            ci = cpus[i]
            co = cpus[(i+4)%5]
            if ci.needs_input() and co.has_output():
                if i == 0:
                    # Remember last known output from the last CPU
                    res = co.output()
                    ci.give_input(res)
                else:
                    ci.give_input(co.output())
                
        # Update all running
        one_running = False
        for c in cpus:
            if not c.is_halted():
                one_running = True

    # Grab the last output from the last CPU if available
    if cpus[4].has_output:
        res = cpus[4].output()
    
    return res
    
assert(thrust_from_phase([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729)
assert(thrust_from_phase([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216)

def find_max_thrust(m):
    res = 0
    for a in range(5):
        for b in filter(lambda x: x not in [a], range(5)):
            for c in filter(lambda x: x not in [a,b], range(5)):
                for d in filter(lambda x: x not in [a,b,c], range(5)):
                    for e in filter(lambda x: x not in [a,b,c,d], range(5)):
                        t = thrust_from_phase(m, [a+5,b+5,c+5,d+5,e+5])
                        if t > res:
                            res = t
    return res

assert(find_max_thrust([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]) == 139629729)
assert(find_max_thrust([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]) == 18216)

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
