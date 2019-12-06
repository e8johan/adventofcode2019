#/usr/bin/env python3

class IntPuter:
    def __init__(self, m, i):
        self.m = m.copy()
        self.i = m.copy()
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
            

cpu = IntPuter([1, 0, 0, 0, 99], [])
cpu.run()
assert(cpu.m == [2, 0, 0, 0, 99])

cpu.reset([2, 3, 0, 3, 99], [])
cpu.run()
assert(cpu.m == [2, 3, 0, 6, 99])

cpu.reset([2, 4, 4, 5, 99, 0], [])
cpu.run()
assert(cpu.m == [2, 4, 4, 5, 99, 9801])

cpu.reset([1, 1, 1, 4, 99, 5, 6, 0, 99], [])
cpu.run()
assert(cpu.m == [30, 1, 1, 4, 2, 5, 6, 0, 99])

cpu.reset([1002, 4, 3, 4, 33], [])
cpu.run()
assert(cpu.m == [1002, 4, 3, 4, 99])

cpu.reset([1101, 100, -1, 4, 0], [])
cpu.run()
assert(cpu.m == [1101, 100, -1, 4, 99])

cpu.reset([3,9,8,9,10,9,4,9,99,-1,8], [8])
cpu.run()
print(cpu.o)
assert(cpu.o == [1])

cpu.reset([3,9,8,9,10,9,4,9,99,-1,8], [7])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,9,7,9,10,9,4,9,99,-1,8], [8])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,9,7,9,10,9,4,9,99,-1,8], [7])
cpu.run()
assert(cpu.o == [1])

cpu.reset([3,3,1108,-1,8,3,4,3,99], [8])
cpu.run()
assert(cpu.o == [1])

cpu.reset([3,3,1108,-1,8,3,4,3,99], [7])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,3,1107,-1,8,3,4,3,99], [8])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,3,1107,-1,8,3,4,3,99], [7])
cpu.run()
assert(cpu.o == [1])

cpu.reset([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [42])
cpu.run()
assert(cpu.o == [1])

cpu.reset([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])
cpu.run()
assert(cpu.o == [0])

cpu.reset([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [42])
cpu.run()
assert(cpu.o == [1])

cpu.reset([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [7])
cpu.run()
assert(cpu.o == [999])

cpu.reset([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [8])
cpu.run()
assert(cpu.o == [1000])

cpu.reset([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [42])
cpu.run()
assert(cpu.o == [1001])

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

cpu.reset(memory, [5])
cpu.run()
print("b: %s" % (cpu.o))
