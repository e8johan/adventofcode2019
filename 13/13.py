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

screen = {}
cpu = IntPuter(memory, [])
o = []
while not cpu.is_halted():
    cpu.step()
    
    while cpu.has_output():
        o.append(cpu.output())
    while len(o) > 3:
        x = o[0]
        y = o[1]
        tile = o[2]
        
        screen[(x,y)] = tile
        
        o = o[3:]

res_a = 0
for k in screen.keys():
    if screen[k] == 2:
        res_a += 1
print("a: %s" % (res_a))

def print_screen(s, b):
    for y in range(20):
        line = ""
        for x in range(36):
            if (x,y) == ball:
                tile = "o"
            else:
                if s[(x, y)] == 0:
                    tile = " "
                elif s[(x, y)] == 1:
                    tile = "#"
                elif s[(x, y)] == 2:
                    tile = "."
                elif s[(x, y)] == 3:
                    tile = "-"
                else: # s[(x, y)] == 4:
                    tile = "O"
            line += tile
        print(line)

screen = {}
score = 0
paddle = (-1, 0)
last_ball = (-1, 0)
ball = (-1, 0)
cleared = []
walls = []
cpu.reset(memory, [])
cpu.m[0] = 2
o = []
while not cpu.is_halted():
    cpu.step()
    
    while cpu.needs_input():
        paddle_target = paddle[0]
        if last_ball != (-1, 0): 
            delta = (ball[0]-last_ball[0], ball[1]-last_ball[1])
            next_ball = (ball[0] + delta[0], ball[1] + delta[1])
            
            if len(cleared) == 2:
                if (ball[0], next_ball[1]) in walls:      # clean bounce, no change in direction
                    delta = (delta[0], -delta[1])
                elif (next_ball[0], ball[1]) in walls:    # side bounce, change of direction
                    delta = (-delta[0], delta[1])
                elif next_ball in walls:                  # edge bounce, change of direction
                    delta = (-delta[0], -delta[1])
            
                next_ball = (ball[0] + delta[0], ball[1] + delta[1])
            
            while len(cleared) > 2:
                if (ball[0], next_ball[1]) in cleared or (ball[0], next_ball[1]) in walls:      # clean bounce, no change in direction
                    if (ball[0], next_ball[1]) in cleared:
                        cleared.remove((ball[0], next_ball[1]))
                    delta = (delta[0], -delta[1])
                elif (next_ball[0], ball[1]) in cleared or (next_ball[0], ball[1]) in walls:    # side bounce, change of direction
                    if (next_ball[0], ball[1]) in cleared:
                        cleared.remove((next_ball[0], ball[1]))
                    delta = (-delta[0], delta[1])
                elif next_ball in cleared or next_ball in walls:                                # edge bounce, change of direction
                    if next_ball in cleared:
                        cleared.remove(next_ball)
                    delta = (-delta[0], -delta[1])
                else:
                    raise Exception("No valid bounce found %s" % (str((paddle, ball, last_ball, paddle_target, cleared))))

                next_ball = (ball[0] + delta[0], ball[1] + delta[1])
            
            if delta[1] == 1:
                if next_ball in screen and screen[next_ball] != 0:
                    paddle_target = ball[0] - delta[0]
                else:
                    paddle_target = ball[0] + delta[0]
            else: # delta < -1
                paddle_target = ball[0] + delta[0]
        
        if paddle_target == -1 or paddle[0] == paddle_target:
            cpu.give_input(0)
        elif paddle[0] < paddle_target:
            cpu.give_input(1)
        else: # paddle > paddle_target
            cpu.give_input(-1)

    cleared = []
    while not (cpu.needs_input() or cpu.is_halted()):
        cpu.step()
        
        while cpu.has_output():
            o.append(cpu.output())
        
        while len(o) > 3:
            x = o[0]
            y = o[1]
            tile = o[2]
            
            if (x, y) == (-1, 0):
                score = tile
            else:
                screen[(x,y)] = tile
                
                if tile == 3:
                    paddle = (x,y)
                elif tile == 4:
                    last_ball = ball
                    ball = (x,y)
                elif tile == 0:
                    cleared.append((x,y))
                elif tile == 1:
                    if not (x,y) in walls:
                        walls.append((x,y))
                
            o = o[3:]
    
#    print(score)
#    print_screen(screen, ball)

# This little >= is probably what made my whole ball tracing function overly complicated
# I constantly miss the last update of the ball, so I have to predict it
while len(o) >= 3:
    x = o[0]
    y = o[1]
    tile = o[2]
    
    if (x, y) == (-1, 0):
        score = tile
    o = o[3:]


print("b: %s" % (score))
