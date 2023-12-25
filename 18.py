import fileinput
from itertools import pairwise

digger_1 = [0, 0] # zeroth = Y = line, first = X = column
digger_2 = [0, 0]
area_1 = 0
area_2 = 0
# shoelace formula, with the extra complication that we need to count the
# perimeter of the area also, but only once.
for line in fileinput.input():
    line_parts = line.rstrip().split()
    direction_1 = line_parts[0]
    length_1 = int(line_parts[1])
    match direction_1:
        case "R":
            cur_line = digger_1[0]
            area_to_top = length_1 * cur_line
            area_without_edge = area_to_top - length_1
            area_1 -= area_without_edge
            digger_1[1] += length_1
        case "L":
            cur_line = digger_1[0]
            area_to_top = length_1 * cur_line
            area_1 += area_to_top
            digger_1[1] -= length_1
        case "U":
            digger_1[0] -= length_1
        case "D":
            area_1 += length_1
            digger_1[0] += length_1

    color = line_parts[2][2:8]
    length_2 = int(color[0:5], 16)
    direction_2 = color[5]
    match direction_2:
        case "0": # R
            cur_line = digger_2[0]
            area_to_top = length_2 * cur_line
            area_without_edge = area_to_top - length_2
            area_2 -= area_without_edge
            digger_2[1] += length_2
        case "2": # L
            cur_line = digger_2[0]
            area_to_top = length_2 * cur_line
            area_2 += area_to_top
            digger_2[1] -= length_2
        case "3": # U
            digger_2[0] -= length_2
        case "1": # D
            area_2 += length_2
            digger_2[0] += length_2

# an off-by-one: i think this is the starting square
area_1 += 1
area_2 += 1

print("part 1:", area_1) #, ", correct:", 62, f"({area_1/62*100:.5f} %)")
print("part 2:", area_2) #, ", correct:", 952408144115, f"({area_2/952408144115*100:.7f} %)")

# part 1 correct with real input: 40745
# part 2 correct with real input: 90111113594927

