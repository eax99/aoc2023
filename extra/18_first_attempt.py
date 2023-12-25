import fileinput
from itertools import pairwise
from sys import exit

# solves part 1 fine with a flood fill, but doesn't solve part 2 correctly:
# i got it to work fine with the test input but not the real input, then when
# fixing it i got it to not work with the test input either, so i'm starting
# over.

def fill_line(dig_map, r1, c1, r2, c2):
    if r1 == r2:
        if c1 < c2:
            for c in range(c1, c2 + 1):
                dig_map[r1][c] = 1
        else:
            for c in range(c2, c1 + 1):
                dig_map[r1][c] = 1
    elif c1 == c2:
        if r1 < r2:
            for r in range(r1, r2 + 1):
                dig_map[r][c1] = 1
        else:
            for r in range(r2, r1 + 1):
                dig_map[r][c1] = 1

# flood fill code adapted from my 10.py.
def flood_fill(bitmap, startrow, startcol):
    width, height = len(bitmap[0]), len(bitmap)
    fill_stack = [(startrow, startcol)]
    while len(fill_stack) > 0:
        bit_row, bit_col = fill_stack.pop()
        if bitmap[bit_row][bit_col] != 0:
            continue
        bitmap[bit_row][bit_col] = 1
        if bit_row - 1 >= 0 and bitmap[bit_row - 1][bit_col] == 0:
            fill_stack.append((bit_row - 1, bit_col))
        if bit_row + 1 < height and bitmap[bit_row + 1][bit_col] == 0:
            fill_stack.append((bit_row + 1, bit_col))
        if bit_col - 1 >= 0 and bitmap[bit_row][bit_col - 1] == 0:
            fill_stack.append((bit_row, bit_col - 1))
        if bit_col + 1 < width and bitmap[bit_row][bit_col + 1] == 0:
            fill_stack.append((bit_row, bit_col + 1))

#####

digger = [0, 0] # zeroth = Y = line, first = X = column
part_1_digger_positions = [tuple(digger)]
part_2_digger = [0, 0]
part_2_digger_positions = [tuple(part_2_digger)]
for line in fileinput.input():
    line_parts = line.rstrip().split()
    direction = line_parts[0]
    dig_length = int(line_parts[1])
    color = line_parts[2][2:8]
    match direction:
        case "R":
            digger[1] += dig_length
        case "L":
            digger[1] -= dig_length
        case "U":
            digger[0] -= dig_length
        case "D":
            digger[0] += dig_length
    part_1_digger_positions.append(tuple(digger))

    pt2_dig_length = int(color[0:5], 16)
    pt2_dig_direction = color[5]
    match pt2_dig_direction:
        case "0": # R
            part_2_digger[1] += pt2_dig_length
        case "1": # D
            part_2_digger[0] += pt2_dig_length
        case "2": # L
            part_2_digger[1] -= pt2_dig_length
        case "3": # U
            part_2_digger[0] -= pt2_dig_length
    part_2_digger_positions.append(tuple(part_2_digger))
    #print(direction, dig_length, color, digger)
#print(part_2_digger_positions)

digger_rows, digger_columns = zip(*part_1_digger_positions)
min_row, max_row = min(digger_rows), max(digger_rows)
min_col, max_col = min(digger_columns), max(digger_columns)
col_offset, row_offset = min_col, min_row
width_columns = max_col - min_col + 1
height_rows = max_row - min_row + 1
dig_map_1 = []
for _ in range(height_rows):
    dig_map_1.append([0] * width_columns)

prev_row, prev_col = part_1_digger_positions[0]
for (row, col) in part_1_digger_positions[1:]:
    # transform digger coordinates into bitmap coordinates
    _row, _prow = row - row_offset, prev_row - row_offset
    _col, _pcol = col - col_offset, prev_col - col_offset
    fill_line(dig_map_1, _row, _col, _prow, _pcol)
    prev_row, prev_col = row, col

# i had a look at the bitmap itself: it's safe to start a flood fill
# at 1, 1 (with the correction applied, of course), and that fill will
# fill the entirety of the inside of the loop.
flood_fill(dig_map_1, 1 - row_offset, 1 - col_offset)
part1 = sum(map(sum, dig_map_1))
print("part 1:", part1)

# a bitmap printout; see extra/18a.png
#dig_map_1[0 - row_offset][0 - col_offset] = 3
#for line in dig_map_1:
#    print("".join(map(lambda n: ".wo#"[n], line)))

exit(0)

# part 2: the lengths and the areas are much, much bigger.
#
# in my case, even with the test input part 2 requires 1_186_329 x 1_186_329,
# or about 1.4 teraelements. i don't have the memory for that.
# test input part 2: min_col 0 max_col 1186328 / min_row 0 max_row 1186328
# with the real input, i need 16972821 x 16181219 = approx 275 teraelements.
# part 2: min_col -1219812 max_col 15753008 / min_row -7178418 max_row 9002800
#
# flood filling is now intractable, but because the polygon traced by the
# digger appears to be simple (and axis-aligned and rectilinear), we can
# use the shoelace algorithm to compute the area.

# first we get rid of those pesky negative coordinates.
digger_rows, digger_columns = zip(*part_2_digger_positions)
min_row, max_row = min(digger_rows), max(digger_rows)
min_col, max_col = min(digger_columns), max(digger_columns)
col_offset, row_offset = min_col, min_row
offset_positions = list(map(
    lambda t: (t[0] - row_offset, t[1] - col_offset), part_2_digger_positions
    ))
#offset_positions.append(offset_positions[0])
#print(offset_positions)

# the total area is calculated by summing up the areas between each horizontal
# element and the top of the picture (row 0). horizontal elements going one
# way are counted as positive area, and those going the other way are counted
# as negative area. the effect is that the negative area will exactly subtract
# the part of the image outside the traced loop, and we will be left with the
# area of the loop itself -- or its negative, if we get the signs wrong.
# we need to take some extra care, though, since in our case the lines
# themselves also have some area; in order to avoid undercounting we need
# to add the thickness of the line back in at some points.
total_area = 0
for ((r0, c0), (r1, c1)) in pairwise(offset_positions):
#    if c0 == c1:
#        if r0 < r1:
#            total_area -= r0 - r1
#        continue # this is a vertical element that adds no area
#    assert r0 == r1
    if c0 > c1:
        # right-to-left edge (c1---c0), providing positive area
        element_area = (c0 - c1) * r0
        # add the edge itself to the positive area
        element_area += c0 - c1
    elif c0 < c1:
        # left-to-right edge (c0---c1), providing negative area
        element_area = (c0 - c1) * r0
        # remove the edge itself from the negative area
        element_area += c1 - c0
    else:
        element_area = 0
    print((r0, c0), (r1, c1), element_area)
    total_area += element_area
        
print("part 2:", total_area)
# 952408144115 is the correct part 2 area of the test input;
# i want to quickly see whether i'm going under or over.
print(952408144115, "-", total_area, "=", 952408144115 - total_area, f"| {total_area/952408144115*100:.07f} %")

#print("part 2 requires a bitmap of", width_columns, "x", height_rows, "=", width_columns * height_rows, "elements")
#print("part 2:", "min_col", min_col, "max_col", max_col, "/", "min_row", min_row, "max_row", max_row)

#print(part_2_digger_positions)

