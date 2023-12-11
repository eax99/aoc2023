infile = open("inputs/10", "r")
#infile = open("tests/10c", "r")
intext = infile.read().rstrip()
intextparts = intext.split("\n")

width = len(intextparts[0])
height = len(intextparts)

# this will be an array of arrays of pairs of pairs, each pair pointing to the
# two neighbors of that square. ground tiles are coded as None and the S is "S".
the_map = []
the_S = (None, None)
the_chars = {} # storing non-ground characters here also, indexed by (row, col)

# the bitmap is for part 2, where we need to figure out the area inside the
# loop. the problem description specifies that the pipes, represented by the
# input data's characters, are only half inside the loop: two parallel pipe
# characters next to each other doesn't count as a barrier, they need to
# actually connect to count as the inside or outside. to avoid complicating
# the floodfill i will be drawing the actual pipes in the bitmap, but we need
# to increase resolution threefold for this to work: each input character will
# match a 3-by-3 square in the bitmap.
the_bitmap = []
for (linenum, line) in enumerate(intextparts):
    map_line = []
    bitmap_lines = [[], [], []]
    for (colnum, char) in enumerate(line):
        line_north = linenum - 1
        line_south = linenum + 1
        char_east = colnum + 1
        char_west = colnum - 1
        if char == "S":
            the_S = (linenum, colnum)
            map_line.append(tuple("S"))
        elif char == "|":
            map_line.append(((line_north, colnum), (line_south, colnum)))
        elif char == "-":
            map_line.append(((linenum, char_west), (linenum, char_east)))
        elif char == "L":
            map_line.append(((line_north, colnum), (linenum, char_east)))
        elif char == "J":
            map_line.append(((line_north, colnum), (linenum, char_west)))
        elif char == "7":
            map_line.append(((linenum, char_west), (line_south, colnum)))
        elif char == "F":
            map_line.append(((linenum, char_east), (line_south, colnum)))
        else:
            map_line.append(None)
        for i in range(3):
            bitmap_lines[i] += ['.', '.', '.']
        if char != ".":
            the_chars[(linenum, colnum)] = char
    the_map.append(map_line)
    the_bitmap += bitmap_lines

#print(width, height)
#print(the_S)
#print(*the_map, sep="\n")


def mark_wall(position, char):
    global the_bitmap
    row = position[0] * 3
    col = position[1] * 3
    #print(position, char, f"[{row}:{row+3}]", f"[{col}:{col+3}]")
    if char == "|":
        the_bitmap[row + 0][col:col+3] = ['.','#','.']
        the_bitmap[row + 1][col:col+3] = ['.','#','.']
        the_bitmap[row + 2][col:col+3] = ['.','#','.']
    elif char == "-":
        the_bitmap[row + 0][col:col+3] = ['.','.','.']
        the_bitmap[row + 1][col:col+3] = ['#','#','#']
        the_bitmap[row + 2][col:col+3] = ['.','.','.']
    elif char == "L":
        the_bitmap[row + 0][col:col+3] = ['.','#','.']
        the_bitmap[row + 1][col:col+3] = ['.','#','#']
        the_bitmap[row + 2][col:col+3] = ['.','.','.']
    elif char == "J":
        the_bitmap[row + 0][col:col+3] = ['.','#','.']
        the_bitmap[row + 1][col:col+3] = ['#','#','.']
        the_bitmap[row + 2][col:col+3] = ['.','.','.']
    elif char == "7":
        the_bitmap[row + 0][col:col+3] = ['.','.','.']
        the_bitmap[row + 1][col:col+3] = ['#','#','.']
        the_bitmap[row + 2][col:col+3] = ['.','#','.']
    elif char == "F":
        the_bitmap[row + 0][col:col+3] = ['.','.','.']
        the_bitmap[row + 1][col:col+3] = ['.','#','#']
        the_bitmap[row + 2][col:col+3] = ['.','#','.']
    else:
        print("unknown char", char, "at position", position)

# find out what char the S was sitting on
s_row, s_col = the_S
north_of_S = the_map[s_row - 1][s_col]
south_of_S = the_map[s_row + 1][s_col]
west_of_S = the_map[s_row][s_col - 1]
east_of_S = the_map[s_row][s_col + 1]

S_could_be = []
if north_of_S != None and the_S in north_of_S:
    S_could_be.append({"|","L","J"})
if south_of_S != None and the_S in south_of_S:
    S_could_be.append({"|","7","F"})
if west_of_S != None and the_S in west_of_S:
    S_could_be.append({"-","7","J"})
if east_of_S != None and the_S in east_of_S:
    S_could_be.append({"-","L","F"})
intersection = S_could_be[0].intersection(*S_could_be[1:])
S_char = list(intersection)[0]

S_tuple = None
if S_char == "|":
    S_tuple = ((s_row - 1, s_col + 0), (s_row + 1, s_col + 0))
elif S_char == "-":
    S_tuple = ((s_row - 0, s_col - 1), (s_row + 0, s_col + 1))
elif S_char == "L":
    S_tuple = ((s_row - 1, s_col + 0), (s_row + 0, s_col + 1))
elif S_char == "J":
    S_tuple = ((s_row - 1, s_col + 0), (s_row + 0, s_col - 1))
elif S_char == "7":
    S_tuple = ((s_row + 1, s_col + 0), (s_row + 0, s_col - 1))
else: # elif S_char == "F":
    S_tuple = ((s_row + 1, s_col + 0), (s_row + 0, s_col + 1))

mark_wall(the_S, S_char)

route_A_prev = the_S
route_A_next = S_tuple[0]
route_A_visited = [the_S]
route_B_prev = the_S
route_B_next = S_tuple[1]
route_B_visited = [the_S]
#the_bitmap[route_A_next[0]][route_A_next[1]] = 'w'
#the_bitmap[route_B_next[0]][route_B_next[1]] = 'w'
mark_wall(route_A_next, the_chars[route_A_next])
mark_wall(route_B_next, the_chars[route_B_next])

route_len = 1
while route_A_next not in route_B_visited and route_B_next not in route_A_visited:
    next_A_pair = the_map[route_A_next[0]][route_A_next[1]]
    next_B_pair = the_map[route_B_next[0]][route_B_next[1]]
    #print(route_A_next, next_A_pair, route_B_next, next_B_pair)
    index_of_prev_A = next_A_pair.index(route_A_prev)
    index_of_prev_B = next_B_pair.index(route_B_prev)
    other_A = next_A_pair[1 - index_of_prev_A]
    other_B = next_B_pair[1 - index_of_prev_B]
    route_A_visited.append(other_A)
    route_B_visited.append(other_B)
    route_A_prev = route_A_next
    route_B_prev = route_B_next
    route_A_next = other_A
    route_B_next = other_B
    #print("A:", route_A_prev, "->", route_A_next, " B:", route_B_prev, "->", route_B_next)
    route_len += 1
    # mark walls for part 2
    mark_wall(route_A_next, the_chars[route_A_next])
    mark_wall(route_B_next, the_chars[route_B_next])
    #the_bitmap[route_A_next[0]][route_A_next[1]] = 'w'
    #the_bitmap[route_B_next[0]][route_B_next[1]] = 'w'
#print(list(sorted(route_A_visited)), list(sorted(route_B_visited)))
#print(*map(lambda l: "".join(l), the_bitmap), sep="\n") # unfilled bitmap
#print("part 1:", route_len) # done at 07:47 UTC+2
# part 2 break at 07:56 UTC+2, resume at 16:20

# the strategy is to do a floodfill on the_bitmap (which isn't a real bitmap
# but an array of arrays of chars). because we drew the bitmap at a higher
# resolution than the given input data, we can get away with starting the fill
# at just one corner: it'll correctly propagate even around wall-adjacent pipe
# sections. after the fill, we then look at the middle character of each 3x3
# box: if not a wall and not marked outside, it must be inside, and we simply
# count those that are inside and get the answer.
bm_width, bm_height = (width * 3, height * 3)
fill_stack = [(0, 0)]
while len(fill_stack) > 0:
    bit_row, bit_col = fill_stack.pop()
    if the_bitmap[bit_row][bit_col] == 'o':
        continue
    the_bitmap[bit_row][bit_col] = 'o'
    if bit_row - 1 >= 0 and the_bitmap[bit_row - 1][bit_col] == '.':
        fill_stack.append((bit_row - 1, bit_col))
    if bit_row + 1 < bm_height and the_bitmap[bit_row + 1][bit_col] == '.':
        fill_stack.append((bit_row + 1, bit_col))
    if bit_col - 1 >= 0 and the_bitmap[bit_row][bit_col - 1] == '.':
        fill_stack.append((bit_row, bit_col - 1))
    if bit_col + 1 < bm_width and the_bitmap[bit_row][bit_col + 1] == '.':
        fill_stack.append((bit_row, bit_col + 1))
print(*map(lambda l: "".join(l), the_bitmap), sep="\n") # filled bitmap
print()
bitmap_square_centers = [bitmap_row[1::3] for bitmap_row in the_bitmap[1::3]]
#print(*map(lambda l: "".join(l), bitmap_square_centers), sep="\n")
inside = 0
for row in bitmap_square_centers:
    for col in row:
        if col == '.':
            inside += 1
#print("part 2:", inside) # done at 17:06 UTC+2
