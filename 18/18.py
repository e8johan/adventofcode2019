#/usr/bin/env python3

def find_paths(world):
    res = {}
    paths = []
    doors = {}
    keys = {}
    for y in range(len(world)):
        for x in range(len(world[y])):
            tile = world[y][x]
            if tile == "@":
                res["start"] = (x,y)
                paths.append((x,y))
            elif tile == ".":
                paths.append((x,y))
            elif tile == "#":
                pass
            else:
                if tile.isupper():
                    doors[tile] = ((x,y))
                else:
                    keys[tile] = ((x,y))
    res["paths"] = paths
    res["doors"] = doors
    res["keys"] = keys
    return res

def moves(point):
    return [(point[0]-1, point[1]), (point[0]+1, point[1]), (point[0], point[1]-1), (point[0], point[1]+1)]

def find_distances(start, paths, keys, limit):
    # unlocked and picked keys
    unlocked = []
    picked = []
    for k in keys:
        if k.upper() in paths["doors"].keys():
            unlocked.append(paths["doors"][k.upper()])
        picked.append(paths["keys"][k])
        
    print(keys)
    
    # resulting distance dict
    ds = {}
    
    distance = 0
    tovisit = [start]
    while len(tovisit) > 0:
        tovisitnext = []
        for v in tovisit:
            ds[v] = distance
        for v in tovisit:
            for w in moves(v):
                if w not in ds.keys():
                    if w in paths["paths"] or w in unlocked or w in picked:
                        tovisitnext.append(w)
        distance += 1
        tovisit = tovisitnext
        
        if distance > limit and limit > 0:
            return {}
                        
    
    #ds[start] = 0
    
    ## initialize with possible moves
    #tovisit = []
    #for v in moves(start):
        #if v not in ds.keys():
            #if v in paths["paths"] or v in unlocked or v in picked:
                #tovisit.append(v)
    
    #while len(tovisit) > 0:
        ## pick next move
        #visit = tovisit[0]
        #tovisit = tovisit[1:]
        
        ## update distances
        #mindistance = -1
        #for v in moves(visit):
            #if v in ds.keys():
                #if mindistance == -1 or mindistance > ds[v]:
                    #mindistance = ds[v]
        #assert mindistance != -1
        #ds[visit] = mindistance+1
        
        ## find possible further moves
        #for v in moves(visit):
            #if v not in ds.keys():
                #if v in paths["paths"] or v in unlocked or v in picked:
                    #tovisit.append(v)

    res = {}
    for k in paths["keys"]:
        if k not in keys:
            for v in moves(paths["keys"][k]):
                if v in ds.keys():
                    res[k] = ds[v]+1

    return res

def solve(world):
    paths = find_paths(world)
    res = _solve(paths, paths["start"], [], -1, 0)
    print(res)
    return res
    
def _solve(paths, position, keys, limit, current):
    if len(paths["keys"]) == len(keys):
        return 0

    pos = position

    distances = find_distances(pos, paths, keys, limit - current)
    
    res = limit
    for k in paths["keys"].keys():
        if k in distances:
            r = _solve(paths, paths["keys"][k], keys + [k], res, distances[k]) + distances[k]
            if res == -1 or r < res:
                res = r
    return res


l1 = ["#########", 
      "#b.A.@.a#", 
      "#########"]

l2 = ["########################", 
      "#f.D.E.e.C.b.A.@.a.B.c.#", 
      "######################.#", 
      "#d.....................#", 
      "########################"]

l3 = ["########################", 
      "#...............b.C.D.f#", 
      "#.######################", 
      "#.....@.a.B.c.d.A.e.F.g#", 
      "########################"]

l4 = ["#################",
      "#i.G..c...e..H.p#",
      "########.########",
      "#j.A..b...f..D.o#",
      "########@########",
      "#k.E..a...g..B.n#",
      "########.########",
      "#l.F..d...h..C.m#",
      "#################"]

l5 = ["########################",
      "#@..............ac.GI.b#",
      "###d#e#f################",
      "###A#B#C################",
      "###g#h#i################",
      "########################"]

assert solve(l1) == 8
assert solve(l2) == 86
assert solve(l3) == 132
#assert solve(l4) == 136
assert solve(l5) == 81

lines = []
while True:
    try:
        line = input()

        lines.append(line)

    except ValueError:
        break
    except EOFError:
        break

print("a: %s" % (solve(lines)))
