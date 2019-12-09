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

cpu = IntPuter([], [])
cpu.reset([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [])
cpu.run()
assert(cpu.o == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])

cpu.reset([1102,34915192,34915192,7,4,7,99,0],[])
cpu.run()
print(cpu.o)
assert(cpu.o == [1219070632396864])

cpu.reset([104,1125899906842624,99], [])
cpu.run()
assert(cpu.o == [1125899906842624])


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

cpu.reset(memory, [1])
cpu.run()
print("a: %s" % (cpu.o))
cpu.reset(memory, [2])
cpu.run()
print("b: %s" % (cpu.o))
