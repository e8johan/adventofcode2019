#/usr/bin/env python3

# This is my input
startingValue = 128392 
endingValue = 643281

value = startingValue

#while True:

# Convert to individual numbers
ns = [int(i) for i in str(value)]
count = 0
while True:
    # The number finder loop - finds the next possible number
    while True:
        # Increase the number
        pos = 1
        while ns[-pos] == 9:
            pos += 1
        ns[-pos] += 1
        while pos > 1:
            pos -= 1
            ns[-pos] = ns[-pos-1]

        # Check for neighbours
        pos = 0
        found = False
        while pos < 5:
            if ns[pos] == ns[pos+1]:
                found = True
                break
            pos += 1
        
        # Ensure increase
        pos = 0
        while pos < 5:
            if ns[pos] > ns[pos+1]:
                found = False
                break
            pos += 1

        if found:
            break

    # Re-assemble the number
    value = 0
    for n in ns:
        value = value*10 + n

    # Check if we're done
    if value < endingValue:
        count += 1
    else:
        break

print("Number of numbers: %s" % (count))
