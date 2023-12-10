import fileinput
from math import lcm
from operator import mul
from itertools import chain
lr_instruction = []
firstpart = True
mapping = {}
a_nodes = []
for line in fileinput.input():
    line = line.rstrip()
    if line == "":
        firstpart = False
        continue
    if firstpart:
        lr_instruction = list(map(lambda c: {"L":0,"R":1}[c], line))
    else:
        key_, parenthesized_val = line.split(" = ")
        val_parts = parenthesized_val[1:-1].split(", ")
        mapping[key_] = tuple(val_parts)
        if key_[2] == "A":
            a_nodes.append(key_)
#print(lr_instruction)
#print(mapping)
#print(a_nodes)

if False: # uncomment to skip part 1
    position = "AAA"
    i = 0
    while position != "ZZZ":
        lr_instruction_index = i % len(lr_instruction)
        direction_to_go = lr_instruction[lr_instruction_index]
        position = mapping[position][direction_to_go]
        #print(position)
        i += 1
    print("part 1:", i) # done at 07:12 UTC+2

def part_2_win_condition(nodelist):
    for node in nodelist:
        if node[2] != "Z":
            return False
    return True

def find_cycle_length(node):
    k = 0
    while node[2] != "Z":
        lr_instruction_index = k % len(lr_instruction)
        direction_to_go = lr_instruction[lr_instruction_index]
        node = mapping[node][direction_to_go]
        k += 1
    return k

cycle_lengths = []
for node in a_nodes:
    cycle_length = find_cycle_length(node)
    print(node, cycle_length)
    cycle_lengths.append(cycle_length)
product = 1
for c in cycle_lengths:
    product *= c
print("part 2:", lcm(*cycle_lengths), product) # done at 07:34 UTC+2

#j = 0
#simultaneous_positions = a_nodes
#print(simultaneous_positions, j)
#while not part_2_win_condition(simultaneous_positions):
#    new_positions = []
#    lr_instruction_index = j % len(lr_instruction)
#    direction_to_go = lr_instruction[lr_instruction_index]
#    for node in simultaneous_positions:
#        new_positions.append(mapping[node][direction_to_go])
#    simultaneous_positions = new_positions
#    print(simultaneous_positions, j + 1)
#    j += 1
#print("part 2:", j) # intractable, will take years
print()
