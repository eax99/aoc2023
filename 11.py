from itertools import combinations
infile = open("inputs/11", "r")
#infile = open("tests/11", "r")
intext = infile.read().rstrip()
intextparts = intext.split("\n")

universe_width = len(intextparts[0])
universe_height = len(intextparts[1])

galaxies_uncorrected = set()
for (linenum, line) in enumerate(intextparts):
    for (col, char) in enumerate(line):
        if char == '#':
            galaxies_uncorrected.add((linenum, col))

columns_present = set([g[1] for g in galaxies_uncorrected])
rows_present = set([g[0] for g in galaxies_uncorrected])
rows_not_present = list(sorted(set(range(universe_height)) - rows_present))
columns_not_present = list(sorted(set(range(universe_width)) - columns_present))

def dimensional_correction(n, absentlist, factor=1):
    num_absent_before_n = len(list(filter(lambda c: c < n, absentlist)))
    return n + num_absent_before_n * factor

def column_correction(n):
    return dimensional_correction(n, columns_not_present)

def row_correction(n):
    return dimensional_correction(n, rows_not_present)

def correct_galaxy_part_1(g):
    return (row_correction(g[0]), column_correction(g[1]))

def correct_galaxy_part_2(g):
    return (
        dimensional_correction(g[0], rows_not_present, 999_999),
        dimensional_correction(g[1], columns_not_present, 999_999)
        )

galaxies = []
part_2_galaxies = []
for galaxy in galaxies_uncorrected:
    galaxies.append(correct_galaxy_part_1(galaxy))
    part_2_galaxies.append(correct_galaxy_part_2(galaxy))

def measure_distance(g1, g2):
    horiz_distance = abs(g1[1] - g2[1])
    vert_distance = abs(g1[0] - g2[0])
    return horiz_distance + vert_distance

total_distance = 0
for (g1, g2) in combinations(galaxies, 2):
    total_distance += measure_distance(g1, g2)
print("part 1:", total_distance) # 07:24 UTC+2

total_distance_part_2 = 0
for (g1, g2) in combinations(part_2_galaxies, 2):
    total_distance_part_2 += measure_distance(g1, g2)
print("part 2:", total_distance_part_2) # 07:29 UTC+2

