#/usr/bin/env python3

nodes = {}

class Node:
    def __init__(self, name, parent_node):
        self.name = name
        self.parent = parent_node
        self.children = []
        
        assert (name not in nodes)
        nodes[name] = self
        
        if self.parent:
            self.parent.add_child(self)

    def set_parent(self, parent_node):
        assert (self.parent == None or self.parent == parent_node)
        
        if self.parent == None:
            self.parent = parent_node
            self.parent.add_child(self)
    
    def add_child(self, child_node):
        self.children.append(child_node)

def distance_to_root(node):
    res = []
    while node.parent:
        node = node.parent
        res.append(node.name)
    return res

def orbits():
    res = 0
    for k, n in nodes.items():
        res += len(distance_to_root(n))
    return res

def orbit_distance(nn1, nn2):
    tr1 = distance_to_root(nodes[nn1])
    tr2 = distance_to_root(nodes[nn2])
    
    while tr1[-1] == tr2[-1]:
        tr1 = tr1[:-1]
        tr2 = tr2[:-1]
    
    return len(tr1) + len(tr2)

memory = []
while True:
    try:
        line = input()

        if line == "":
            break

        ns = line.split(")")
        parent_name = ns[0]
        child_name = ns[1]
        if parent_name in nodes:
            pn = nodes[parent_name]
        else:
            pn = Node(parent_name, None)
        
        if child_name in nodes:
            cn = nodes[child_name]
            cn.set_parent(pn)
        else:
            cn = Node(child_name, pn)
        
        # each node can only have one parent... I guess that is important here...

    except ValueError:
        break
    except EOFError:
        break

print("Orbits (a): %s" % (orbits()))
print("Orbital distance (b): %s" % (orbit_distance('SAN', 'YOU')))
