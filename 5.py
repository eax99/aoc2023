import fileinput
from operator import itemgetter
infile = open("inputs/5", "r")
#infile = open("tests/5", "r")
intext = infile.read().rstrip()
intextparts = intext.split("\n\n")

seeds_to_plant = list(map(int, intextparts[0].split()[1:]))
seed_range_pairs = list(sorted(list(zip(seeds_to_plant[0::2], seeds_to_plant[1::2]))))
seed_pairs_first_last = list(map(lambda tup: (tup[0], tup[0]+tup[1]-1), seed_range_pairs))
#print(seed_pairs_first_last)

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
maps = [
    seed_to_soil_map, soil_to_fert_map, fert_to_water_map, water_to_light_map,
    light_to_temp_map, temp_to_hum_map, hum_to_loc_map
    ]
map_names = [
    "seed to soil", "soil to fertilizer", "fertilizer to water",
    "water to light", "light to temperature", "temperature to humidity",
    "humidity to location"
    ]
first_last_maps = []
for (i, map_) in enumerate(maps):
    flmap = []
    for (dest, source, range_len) in sorted(map_, key=itemgetter(1)):
        flmap.append((source, source + range_len - 1, dest - source))
    first_last_maps.append(list(sorted(flmap)))
#print(*first_last_maps, sep="\n")
#print("^ first_last_maps")

def map_number(innum, the_map):
    for (dest_start, source_start, range_len) in the_map:
        if innum in range(source_start, source_start + range_len):
            innum_offset = innum - source_start
            return dest_start + innum_offset
    return innum

def thru_map(seed_num):
    num = seed_num
    for map_ in maps:
        num = map_number(num, map_)
    return num

inflection_points = set()
for (dest, source, range_) in sum(maps, start=[]):
    inflection_points.add(source)
    inflection_points.add(dest)
inflection_points = list(sorted(inflection_points))

def apply_map_rule(contiguous_range, map_rule):
    unmapped_start = tuple()
    mapped_middle = tuple()
    unmapped_end = tuple()
    m_first, m_last, m_offset = map_rule
    r_first, r_last = contiguous_range
    #print(contiguous_range, r_first, r_last)
    #print(map_rule, m_first, m_last, m_offset)
    if m_first > r_last or m_last < r_first:
        #print(1)
        # rule does not apply for this range
        unmapped_end = (r_first, r_last)
    elif m_first <= r_first and m_last >= r_last:
        #print(2)
        # rule applies over the entire range
        mapped_middle = (r_first + m_offset, r_last + m_offset)
    elif m_first <= r_first and m_last < r_last:
        #print(3)
        # rule applies over the first half of the range, so it's split into two
        mapped_middle = (r_first + m_offset, m_last + m_offset)
        unmapped_end = (m_last + 1, r_last)
    elif m_first > r_first and m_last >= r_last:
        #print(4)
        # rule applies over the second half of the range, so it's split in two
        unmapped_start = (r_first, m_first - 1)
        mapped_middle = (m_first + m_offset, r_last + m_offset)
    else:
        #print(5)
        # rule applies over some middle section of the range, so it's split in three
        unmapped_start = (r_first, m_first - 1)
        mapped_middle = (m_first + m_offset, m_last + m_offset)
        unmapped_end = (m_last + 1, r_last)
    return (unmapped_start, mapped_middle, unmapped_end)

def apply_mapset_to_range(contiguous_range, mapset):
    # we need to decide which parts of our range are affected by any rule.
    # rules don't overlap, but they might be right next to each other.
    # our apply_map_rule returns a triplet: the zeroth and second parts are
    # the unmapped start and end portion of the contiguous range component,
    # and the first (middle) part is the mapped component.
    # since our mapping rules are sorted by starting element,
    # we can proceed left to right/lowest to highest,
    # keeping the mapped middle and passing the unmapped right to the next rule.
    components = []
    next_iter_input = contiguous_range
    for (rulenum, rule) in enumerate(mapset):
        first, middle, right = apply_map_rule(next_iter_input, rule)
        #print("rule", rulenum, rule, "mapped", next_iter_input, "to", first, middle, right)
        if len(first) > 0:
            components.append(first)
        if len(middle) > 0 and len(right) == 0:
            components.append(middle)
            next_iter_input = ()
            break
        elif len(middle) > 0:
            components.append(middle)
        next_iter_input = right
    if len(next_iter_input) > 0:
        components.append(next_iter_input)
#        if mapped_component_parts == [component]:
#            pass # no change
#        else:
#            print("mapset", mapsetnum, "rule", rulenum, rule, "turned", component, "into", mapped_component_parts)
#            mapped_range += mapped_component_parts
#            break
    return components

absolute_minimum_location_number = float("+Infinity")
for seed_range in seed_pairs_first_last:
    seed_range = [seed_range]
    minimum = float("+Infinity")
    for (mapsetnum, mapset) in enumerate(first_last_maps):
    #    print("mapset:", mapsetnum, "seed range:", seed_range)
        mapped_range = []
        for component in seed_range:
            mapped_components = apply_mapset_to_range(component, mapset)
            mapped_range += mapped_components
    #    if len(mapped_range) == 0:
    #        print("mapset", mapsetnum, "applied no changes to range")
    #    print("mapped range:", mapped_range, list(zip(*mapped_range)))
        mapped_range.sort()
        seed_range = mapped_range
    (range_starts, range_ends) = list(zip(*seed_range))
    minimum_range_start = min(range_starts)
    #print("seed range:", seed_range, "minimum:", minimum_range_start, "\n")
    if minimum_range_start < absolute_minimum_location_number:
        absolute_minimum_location_number = minimum_range_start

print("part 2:", absolute_minimum_location_number)

#print(seeds_to_plant, seed_to_soil_map, soil_to_fert_map, fert_to_water_map, water_to_light_map, light_to_temp_map, temp_to_hum_map, hum_to_loc_map, sep="\n")
smallest = float("+Infinity")
#print(len(seeds_to_plant), "numbers in seeds line,", len(seeds_to_plant)//2, "pairs")
for n in seeds_to_plant:
    #print(map_number(n, seed_to_soil_map), thru_map(n))
    loc = thru_map(n)
    if loc < smallest:
        smallest = loc
print("part 1:", smallest) # done at 07:22 UTC+2

from sys import exit
exit(0)

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

#print(seed_to_soil_map, soil_to_fert_map, sep="\n", end="\n\n")
ultimate_function = []
for (dest, source, range_) in seed_to_soil_map:
    ultimate_function.append((source, source+range_, dest - source))
ultimate_function = rationalize(ultimate_function)
#print(ultimate_function)
for (first, last, range_) in sorted(map(range_cvt, soil_to_fert_map)):
    ultimate_function.append((first, last, range_))
ultimate_function = rationalize(ultimate_function)


#print(ultimate_function)

#print(seeds_to_plant)
#print(list(seed_range_pairs))
smallest = float("+Infinity")
i = 0
for (seed_start, range_len) in seed_range_pairs:
    print((seed_start, range_len))
    for n in range(seed_start, seed_start + range_len):
        loc = thru_map(n)
        if loc < smallest:
            smallest = loc
            print(smallest)
print("part 2:", smallest) # done and realized intractable at 07:28

print()
