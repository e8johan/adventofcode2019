#/usr/bin/env python3

class Image:
    def __init__(self, width, height, data):
        self.w = width
        self.h = height
        self.d = data
        
    def layers(self):
        return int(len(self.d)/(self.w*self.h))

    def layer(self, layer):
        layer_size = self.w*self.h
        return self.d[layer*layer_size:(layer+1)*layer_size]

    def occurences(self, layer_index, pixel):
        count = 0
        for p in self.layer(layer_index):
            if p == pixel:
                count += 1
        return count
    
    def flatten(self):
        rows = []
        l = self.layer(0)
        for r in range(int(len(l)/self.w)):
            rows.append(l[r*self.w:(r+1)*self.w])
        for li in range(1, self.layers()):
            l = self.layer(li)
            for r in range(int(len(l)/self.w)):
                row = l[r*self.w:(r+1)*self.w]
                for pi in range(len(row)):
                    if rows[r][pi] == "2":
                        rows[r] = rows[r][:pi] + row[pi] + rows[r][pi+1:]
        return rows

i = Image(3, 2, "123456789012")
assert(i.layers() == 2)
assert(i.layer(0) == "123456")
assert(i.layer(1) == "789012")

i = Image(25, 6, input())

zerolayer = -1
minzeroes = 0
for li in range(i.layers()):
    zeroes = i.occurences(li, "0")
    if zerolayer == -1 or zeroes < minzeroes:
        zerolayer = li
        minzeroes = zeroes

ones = i.occurences(zerolayer, "1")
twos = i.occurences(zerolayer, "2")
print("%s: %s*%s = %s" % (zerolayer, ones, twos, ones*twos))
for r in i.flatten():
    print(r.replace("0", " ").replace("1", "X"))
