#/usr/bin/env python3

def sequence(pos, length):
    base = [0, 1, 0, -1]
    res = []
    
    # repeat each value based on pos
    for v in base:
        for i in range(pos+1):
            res.append(v)
    
    # extend until long enough
    while len(res) < length:
        res = res+res
    
    # skip first value
    res = res[1:] + [res[0]]
    
    return res

assert sequence(0,0) == [1,0,-1,0]
assert sequence(1,0) == [0,1,1,0,0,-1,-1,0]

def calc_pos(signal, pos):
    res = 0
    pattern = sequence(pos, len(signal))
    for i in range(len(signal)):
        res += signal[i] * pattern[i]

    return abs(res) % 10

assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 0) == 4
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 1) == 8
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 2) == 2
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 3) == 2
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 4) == 6
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 5) == 1
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 6) == 5
assert calc_pos([1, 2, 3, 4, 5, 6, 7, 8], 7) == 8

def calc_phase(signal):
    res = []
    for i in range(len(signal)):
        res.append(calc_pos(signal, i))
    return res

assert calc_phase([1, 2, 3, 4, 5, 6, 7, 8]) == [4, 8, 2, 2, 6, 1, 5, 8]
assert calc_phase([4, 8, 2, 2, 6, 1, 5, 8]) == [3, 4, 0, 4, 0, 4, 3, 8]

def calc_phases(signal, rounds):
    res = signal
    for r in range(rounds):
        res = calc_phase(res)
    
    return res

assert calc_phases([1, 2, 3, 4, 5, 6, 7, 8], 4) == [0, 1, 0, 2, 9, 4, 9, 8]
assert calc_phases([8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5], 100)[:8] == [2,4,1,7,6,1,7,6]
assert calc_phases([1,9,6,1,7,8,0,4,2,0,7,2,0,2,2,0,9,1,4,4,9,1,6,0,4,4,1,8,9,9,1,7], 100)[:8] == [7,3,7,4,5,4,1,8]
assert calc_phases([6,9,3,1,7,1,6,3,4,9,2,9,4,8,6,0,6,3,3,5,9,9,5,9,2,4,3,1,9,8,7,3], 100)[:8] == [5,2,4,3,2,1,3,3]

signal = []
line = input()
for c in line:
    signal.append(int(c))

print("a: %s" % (calc_phases(signal, 100)[:8]))
