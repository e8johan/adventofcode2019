#/usr/bin/env python3

def processor(m):
    pc = 0
    while True:
        if m[pc] == 1:
            m[m[pc+3]] = m[m[pc+1]] + m[m[pc+2]]
        elif m[pc] == 2:
            m[m[pc+3]] = m[m[pc+1]] * m[m[pc+2]]
        elif m[pc] == 99:
            break
        else:
            assert False, "Invalid op code at %s" % (pc)

        pc += 4

    return m


assert(processor([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99])
assert(processor([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99])
assert(processor([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801])
assert(processor([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99])

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

memory[1] = 12
memory[2] = 2

print("memory[0] (a): %s" % (processor(memory.copy())[0]))

for noun in range(0,99):
    for verb in range(0,99):
        memory[1] = noun
        memory[2] = verb
        if processor(memory.copy())[0] == 19690720:
            print("Noun-verb (b): %s" % (noun*100 + verb))
            exit(0)
