import fileinput
import itertools
garden = []
start_pos = []
linenumber = 0
for line in fileinput.input():
    line = line.rstrip()
    numeric_line = list(map(lambda c: [999,0,100]["#.S".index(c)], line))
    if 1 in numeric_line:
        colnumber = numeric_line.index(1)
        start_pos = (linenumber, colnumber)
    garden.append(numeric_line)
    linenumber += 1

def write_garden_image(filename="21.data"):
    outfile = open(filename, "wb")
    joined_garden = itertools.chain.from_iterable(garden)
    int_byte_map = {
        999: bytes.fromhex("000000"),
        0: bytes.fromhex("c1ddd2"),
        100: bytes.fromhex("c30be0")
        }
    for i in range(1, 65):
        int_byte_map[i]=bytes.fromhex(f"{64+2*i:02x}{32:02x}{i%2*160:02x}")
    print_data = b"".join(map(lambda n: int_byte_map[n], joined_garden))
    outfile.write(print_data)
    outfile.close()

def print_garden():
    def num_to_char(n):
        if n == 999: return "#"
        if n == 0: return "."
        if n == 100: return "S"
        idx = n % 2
        return "oO"[idx]
    for numline in garden:
        print("".join(map(num_to_char, numline)))

# garden_update(n) will turn the neighbor of every n square into an n+1
# square, simultaneously. special case for n = 0, where every neighbor
# of 100 (the starting square) is turned into a 1.
def garden_update(iter_number):
    neighbors = set()
    max_line = len(garden)
    max_col = len(garden[0])
    for linenum in range(max_line):
        for colnum in range(max_col):
            if ((iter_number > 0 and garden[linenum][colnum] == iter_number)
                or (iter_number == 0 and garden[linenum][colnum] == 100)):
                if linenum - 1 >= 0 and garden[linenum - 1][colnum] != 999:
                    neighbors.add((linenum - 1, colnum))
                if linenum + 1 < max_line and garden[linenum+1][colnum] != 999:
                    neighbors.add((linenum + 1, colnum))
                if colnum - 1 >= 0 and garden[linenum][colnum - 1] != 999:
                    neighbors.add((linenum, colnum - 1))
                if colnum + 1 < max_col and garden[linenum][colnum + 1] != 999:
                    neighbors.add((linenum, colnum + 1))
    for (l, c) in neighbors:
        garden[l][c] = iter_number + 1
    #write_garden_image(filename=f"21.{iter_number:02}.data")
    #print_garden()

for i in range(64):
    garden_update(i)

joined_garden = itertools.chain.from_iterable(garden)
squares_equal_to_64 = list(map(lambda n: int(n == 64), joined_garden))
#for n in range(len(garden)):
#    print("".join(map(str, squares_equal_to_64[n*len(garden[0]):(n+1)*len(garden[0])])))
print("part 1:", sum(squares_equal_to_64))

