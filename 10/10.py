#/usr/bin/env python3

def map_to_coords(m):
    res = []
    y = 0
    for l in m:
        x = 0
        for c in l:
            if c == "#":
                res.append((x, y))
            x += 1
        y += 1
    return res

assert(map_to_coords(["#..", ".#.", "#.#"]) == [(0,0), (1,1), (0,2), (2,2)])

def observable_coords(x, y, cs):
    res = []
    for c in cs:
        obstructed = False
        if (c[0] == x and c[1] == y):
            obstructed = True
        else:
            for d in cs:
                if not c == d:
                    if c[0] == x and d[0] == x:
                        if (c[1] < d[1] and y > d[1]) or (c[1] > d[1] and y < d[1]):
                            obstructed = True
                    elif c[1] == y and d[1] == y:
                        if (c[0] < d[0] and x > d[0]) or (c[0] > d[0] and x < d[0]):
                            obstructed = True
                    else:
                        dxc = c[0] - x
                        dyc = c[1] - y
                        dxd = d[0] - x
                        dyd = d[1] - y
                        # avoid divide by zero
                        if (dyc == 0 and dyd != 0) or (dyc != 0 and dyd == 0):
                            pass # not obstructed
                        else:
                            if dxc / dyc == dxd / dyd:
                                # on the same angle, which is closer
                                if dxc*dxc + dyc*dyc > dxd*dxd + dyd*dyd:
                                    # d is closer than c, but on which side
                                    if dxc > 0 and dxd > 0:
                                        if dyc > 0 and dyd > 0:
                                            obstructed = True
                                        if dyc < 0 and dyd < 0:
                                            obstructed = True
                                    elif dxc < 0 and dxd < 0:
                                        if dyc > 0 and dyd > 0:
                                            obstructed = True
                                        if dyc < 0 and dyd < 0:
                                            obstructed = True
        if not obstructed:
            res.append(c)
    return res

def observable_from_coord(x, y, cs):
    return len(observable_coords(x, y, cs))

assert(observable_from_coord(1, 0, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(4, 0, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(0, 2, map_to_coords([".#..#",".....","#####","....#","...##"])) == 6)
assert(observable_from_coord(1, 2, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(2, 2, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(3, 2, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(4, 2, map_to_coords([".#..#",".....","#####","....#","...##"])) == 5)
assert(observable_from_coord(4, 3, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)
assert(observable_from_coord(3, 4, map_to_coords([".#..#",".....","#####","....#","...##"])) == 8)
assert(observable_from_coord(4, 4, map_to_coords([".#..#",".....","#####","....#","...##"])) == 7)

def find_best_coord(m):
    cs = map_to_coords(m)
    res_o = 0
    res_c = (0,0)
    for c in cs:
        o = observable_from_coord(c[0], c[1], cs)
        if o > res_o:
            res_o = o
            res_c = c
    return (res_c, res_o)

assert(find_best_coord([".#..#",".....","#####","....#","...##"]) == ((3, 4), 8))

assert(find_best_coord(["......#.#.","#..#.#....","..#######.",".#.#.###..",".#..#.....","..#....#.#","#..#....#.",".##.#..###","##...#..#.",".#....####"]) == ((5,8),33))
assert(find_best_coord(["#.#...#.#.",".###....#.",".#....#...","##.#.#.#.#","....#.#.#.",".##..###.#","..#...##..","..##....##","......#...",".####.###."]) == ((1,2),35))
assert(find_best_coord([".#..#..###","####.###.#","....###.#.","..###.##.#","##.##.#.#.","....###..#","..#.#..#.#","#..#.#.###",".##...##.#",".....#.#.."]) == ((6,3), 41))

def order_a_circle(x, y, m):
    res_m = m.copy()
    res_l = []
    
    for c in observable_coords(x, y, map_to_coords(m)):
        group = -1
        factor = 0
        dx = c[0] - x
        dy = c[1] - y
        if dx >= 0 and dy < 0:
            group = 0
            factor = abs(dx/dy)
        elif dx > 0 and dy >= 0:
            group = 1
            factor = abs(dy/dx)
        elif dx <= 0 and dy > 0:
            group = 2
            factor = abs(dx/dy)
        else:
            group = 3
            factor = abs(dy/dx)
        res_l.append((group, factor, c))

    return sorted(res_l, key=lambda x: (x[0], x[1]))

m = []
while True:
    try:
        line = input()

        if line == "":
            break
        m.append(line)

    except ValueError:
        break
    except EOFError:
        break

r = find_best_coord(m)
print("a: %s" % (r[1]))
vs = order_a_circle(r[0][0], r[0][1], m)
print("b: %s" % (vs[199][2][0]*100+vs[199][2][1]))
