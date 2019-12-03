#/usr/bin/env python3

def move(direction, length):
    resx = 0
    resy = 0

    if direction == 'D':
        resy = length
    elif direction == 'U':
        resy = -length
    elif direction == 'R':
        resx = length
    elif direction == 'L':
        resx = -length
    else:
        assert False, "Unexpected direction '%s'" % (direction)
        
    return resx, resy

def parse_line(line):
    res = []
    
    posx = 0
    posy = 0
    
    for segment in line.split(","):
        d = segment[:1]
        l = int(segment[1:])
        dx, dy = move(d, l)
        res.append((posx, posy, d, l, dx, dy))
        posx += dx
        posy += dy

    return res

assert(parse_line("R75,D30") == [(0, 0, 'R', 75, 75, 0), (75, 0, 'D', 30, 0, 30)])

def find_intersections(l1, l2):
    res = []
    for s1 in l1:
        for s2 in l2:
            if s1[4] == 0:
                # move from s1[0], s1[1] -> s1[0], s1[1] + s1[5]
                if s2[4] == 0:
                    # move from s2[0], s2[1] -> s2[0], s2[1] + s2[5]
                    pass # parallel
                else: # s2[5] == 0
                    # move from s2[0], s2[1] -> s2[0] + s2[4], s2[1]
                    if s1[0] > min(s2[0], s2[0] + s2[4]) and s1[0] < max(s2[0], s2[0] + s2[4]) and s2[1] > min(s1[1], s1[1] + s1[5]) and s2[1] < max(s1[1], s1[1] + s1[5]):
                        res.append((s1[0], s2[1]))
            else: # s1[5] == 0
                # move from s1[0], s1[1] -> s1[0] + s1[4], s1[1]
                if s2[4] == 0:
                    # move from s2[0], s2[1] -> s2[0], s2[1] + s2[5]
                    if s1[1] > min(s2[1], s2[1] + s2[5]) and s1[1] < max(s2[1], s2[1] + s2[5]) and s2[0] > min(s1[0], s1[0] + s1[4]) and s2[0] < max(s1[0], s1[0] + s1[4]):
                        res.append((s2[0], s1[1]))
                else: # s2[5] == 0
                    # move from s2[0], s2[1] -> s2[0] + s2[4], s2[1]
                    pass # parallel
    return res

assert(find_intersections(parse_line("R8,U5,L5,D3"), parse_line("U7,R6,D4,L4")) == [(6,-5),(3,-3)])

def find_closest_distance(l1, l2):
    res = 0
    for i in find_intersections(l1, l2):
        if res == 0 or res > abs(i[0])+abs(i[1]):
            res = abs(i[0])+abs(i[1])
    return res

assert(find_closest_distance(parse_line("R8,U5,L5,D3"), parse_line("U7,R6,D4,L4")) == 6)
assert(find_closest_distance(parse_line("R75,D30,R83,U83,L12,D49,R71,U7,L72"), parse_line("U62,R66,U55,R34,D71,R55,D58,R83")) == 159)
assert(find_closest_distance(parse_line("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"), parse_line("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")) == 135)

print("Distance: %s" % find_closest_distance(parse_line(input()), parse_line(input())))
