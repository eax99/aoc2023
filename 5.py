import fileinput
from operator import itemgetter
#infile = open("inputs/5", "r")
infile = open("tests/5", "r")
intext = infile.read().rstrip()
intextparts = intext.split("\n\n")

seeds_to_plant = list(map(int, intextparts[0].split()[1:]))

def numberify_map(list_of_lines):
    numberify_lambda = lambda s: list(map(int, s.split()))
    return list(map(numberify_lambda, list_of_lines))
seed_to_soil_map = numberify_map(intextparts[1].split("\n")[1:])
soil_to_fert_map = numberify_map(intextparts[2].split("\n")[1:])
fert_to_water_map = numberify_map(intextparts[3].split("\n")[1:])
water_to_light_map = numberify_map(intextparts[4].split("\n")[1:])
light_to_temp_map = numberify_map(intextparts[5].split("\n")[1:])
temp_to_hum_map = numberify_map(intextparts[6].split("\n")[1:])
hum_to_loc_map = numberify_map(intextparts[7].split("\n")[1:])

def map_number(innum, the_map):
    for (dest_start, source_start, range_len) in the_map:
        if innum in range(source_start, source_start + range_len):
            innum_offset = innum - source_start
            return dest_start + innum_offset
    return innum

def thru_map(seed_num):
    soil_num = map_number(seed_num, seed_to_soil_map)
    fert_num = map_number(soil_num, soil_to_fert_map)
    water_num = map_number(fert_num, fert_to_water_map)
    light_num = map_number(water_num, water_to_light_map)
    temp_num = map_number(light_num, light_to_temp_map)
    hum_num = map_number(temp_num, temp_to_hum_map)
    loc_num = map_number(hum_num, hum_to_loc_map)
    return loc_num

#print(seeds_to_plant, seed_to_soil_map, soil_to_fert_map, fert_to_water_map, water_to_light_map, light_to_temp_map, temp_to_hum_map, hum_to_loc_map, sep="\n")
smallest = float("+Infinity")
print(len(seeds_to_plant), "numbers in seeds line,", len(seeds_to_plant)//2, "pairs")
for n in seeds_to_plant:
    #print(map_number(n, seed_to_soil_map), thru_map(n))
    loc = thru_map(n)
    if loc < smallest:
        smallest = loc
print("part 1:", smallest) # done at 07:22 UTC+2

seed_range_pairs = zip(seeds_to_plant[0::2], seeds_to_plant[1::2])
print("total length of ranges:", sum(seeds_to_plant[1::2]))

# map optimization: part 2 has 2,221,837,783 things to check with my input,
# intractable going one-by-one. it's mostly linear math.
# seed_to_soil_map
# soil_to_fert_map
# fert_to_water_map
# water_to_light_map
# light_to_temp_map
# temp_to_hum_map
# hum_to_loc_map
# a map has these (dest, source, range) triplets.
# each means: from [source, source+range[, add an offset of (dest - source).
# these compound over the entire range of the input: we keep splitting it up
# and the function of seed -> location ends up zigzagging around.
def rationalize(func):
    # sort first by last element, then by first
    func = sorted(sorted(func, key=itemgetter(1), reverse=True), key=itemgetter(0))
    newfunc = []
    for (i, (first, last, offset)) in enumerate(func):
        if i == 0:
            newfunc.append((first, last, offset))
            continue
        if newfunc[i-1][1] > first:
            prev_range = newfunc[i-1]
            del newfunc[i-1]
            range_overlap = first - prev_range[1]
            overlap_offset = prev_range[2] + offset
            newfunc.append((prev_range[0], first, prev_range[2]))
            newfunc.append((first, prev_range[1], overlap_offset))
            newfunc.append((prev_range[1], last, offset))
        else:
            newfunc.append((first, last, offset))
    return newfunc
def range_cvt(tup):
    (dest, source, range_) = tup
    return (source, source + range_, dest - source)

print(seed_to_soil_map, soil_to_fert_map, sep="\n", end="\n\n")
ultimate_function = []
for (dest, source, range_) in seed_to_soil_map:
    ultimate_function.append((source, source+range_, dest - source))
ultimate_function = rationalize(ultimate_function)
print(ultimate_function)
for (first, last, range_) in sorted(map(range_cvt, soil_to_fert_map)):
    ultimate_function.append((first, last, range_))
ultimate_function = rationalize(ultimate_function)


print(ultimate_function)

#print(seeds_to_plant)
#print(list(seed_range_pairs))
#smallest = float("+Infinity")
#i = 0
#for (seed_start, range_len) in seed_range_pairs:
#    for n in range(seed_start, seed_start + range_len):
#        loc = thru_map(n)
#        if loc < smallest:
#            smallest = loc
#print("part 2:", smallest) # done and realized intractable at 07:28

print()
