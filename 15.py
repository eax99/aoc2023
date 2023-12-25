import fileinput
import re

def hash_(s):
    v_h = 0
    for c in s:
        v_c = ord(c)
        v_h += v_c
        v_h *= 17
        v_h %= 256
    return v_h

part1 = 0
boxes = {}
for n in range(256):
    boxes[n] = {}

for line in fileinput.input():
    line = line.rstrip()
    initialization_sequence = line.split(",")
    for step in initialization_sequence:
        # part 1
        part1 += hash_(step)
        # part 2
        step_parts = re.split(r'([-=])', step)
        label = step_parts[0]
        boxnum = hash_(label)
        operation = step_parts[1]
        if operation == '-':
            if label in boxes[boxnum]:
                del boxes[boxnum][label]
        else:
            focal_length = int(step_parts[2])
            boxes[boxnum][label] = focal_length
        #print(f"After \"{step}\":")
        #for boxnum in boxes:
        #    if len(boxes[boxnum].items()) > 0:
        #        print("Box", boxnum, boxes[boxnum])
        #print()
print("part 1:", part1)

part2 = 0
for boxnum in boxes:
    for (lens_number, focal_length) in enumerate(boxes[boxnum].values()):
        focusing_power = (boxnum + 1) * (lens_number + 1) * focal_length
        part2 += focusing_power
print("part 2:", part2)
# completed on the last day
