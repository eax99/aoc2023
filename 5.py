import fileinput
from operator import itemgetter
infile = open("inputs/5", "r")
#infile = open("tests/5", "r")
intext = infile.read().rstrip()
intextparts = intext.split("\n\n")

# this is used by part 1 as is
seeds_to_plant = list(map(int, intextparts[0].split()[1:]))
# this is needed in part 2: each (n, m) pair of seeds is actually
# a (start, length) tuple describing a range, and we turn them
# into (start, end) tuples.
# all tuples will be inclusive: the `end` parameter is in the range.
seed_range_pairs = list(sorted(list(zip(seeds_to_plant[0::2], seeds_to_plant[1::2]))))
seed_pairs_first_last = list(map(lambda tup: (tup[0], tup[0]+tup[1]-1), seed_range_pairs))

# processing of all the mappings in the input ###
# we turn them from the "<dest> <source> <len>" textual triplets
# into (source, source+len-1, dest-source) integer triples that
# describe the mapping more directly and are more straightforwardly
# applied to the input seed ranges.

def numberify_map(list_of_lines):
    numberify_lambda = lambda s: list(map(int, s.split()))
    return list(map(numberify_lambda, list_of_lines))

maps = []
for i in range(1, 8):
    # the extra [1:] skips over the line containing the name of the map
    maps.append(numberify_map(intextparts[i].split("\n")[1:]))

first_last_maps = []
for map_ in maps:
    flmap = []
    for (dest, source, range_len) in sorted(map_, key=itemgetter(1)):
        flmap.append((source, source + range_len - 1, dest - source))
    first_last_maps.append(list(sorted(flmap)))

# done with map processing

# functions for part 1: just apply each map in turn to an input number

def apply_map_to_number(innum, the_map):
    for (dest_start, source_start, range_len) in the_map:
        if innum in range(source_start, source_start + range_len):
            innum_offset = innum - source_start
            return dest_start + innum_offset
    return innum

def apply_all_maps_to_number(seed_num):
    num = seed_num
    for map_ in maps:
        num = apply_map_to_number(num, map_)
    return num

# functions for part 2: do the same, but apply each map to an entire
# range of input seed numbers, without computing each individual number.
# the input ranges necessarily get broken up into probably non-contiguous
# sub-ranges.

def apply_map_rule(contiguous_range, map_rule):
    unmapped_start = tuple()
    mapped_middle = tuple()
    unmapped_end = tuple()
    m_first, m_last, m_offset = map_rule
    r_first, r_last = contiguous_range
    if m_first > r_last or m_last < r_first:
        # rule does not apply for this range
        unmapped_end = (r_first, r_last)
    elif m_first <= r_first and m_last >= r_last:
        # rule applies over the entire range
        mapped_middle = (r_first + m_offset, r_last + m_offset)
    elif m_first <= r_first and m_last < r_last:
        # rule applies over the first half of the range, so it's split into two
        mapped_middle = (r_first + m_offset, m_last + m_offset)
        unmapped_end = (m_last + 1, r_last)
    elif m_first > r_first and m_last >= r_last:
        # rule applies over the second half of the range, so it's split in two
        unmapped_start = (r_first, m_first - 1)
        mapped_middle = (m_first + m_offset, r_last + m_offset)
    else:
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
    return components

# optional printout, telling us stuff about the input
print("#", len(seeds_to_plant), "numbers in seeds line,", len(seeds_to_plant)//2, "pairs, total length of seed ranges:", sum(seeds_to_plant[1::2]), ", number of mappings:", sum(map(len, first_last_maps)))

# part 1
smallest = float("+Infinity")
for n in seeds_to_plant:
    loc = apply_all_maps_to_number(n)
    if loc < smallest:
        smallest = loc
print("part 1:", smallest) # done at 07:22 UTC+2

# part 2
# an insight: all the ranges are increasing, so we just need to compute
# what each of the 10 input ranges gets mapped to -- they'll be broken up
# into numerous sub-ranges, but like a-couple-of-dozen-numerous, not
# two-billion-numerous (what brute-forcing would require).
# and since they're all increasing we just need to find the minimum
# of the starting elements of each range.
absolute_minimum_location_number = float("+Infinity")
for seed_range in seed_pairs_first_last:
    seed_range = [seed_range]
    minimum = float("+Infinity")
    for (mapsetnum, mapset) in enumerate(first_last_maps):
        mapped_range = []
        for component in seed_range:
            mapped_components = apply_mapset_to_range(component, mapset)
            mapped_range += mapped_components
        mapped_range.sort()
        seed_range = mapped_range
    (range_starts, range_ends) = list(zip(*seed_range))
    minimum_range_start = min(range_starts)
    if minimum_range_start < absolute_minimum_location_number:
        absolute_minimum_location_number = minimum_range_start

print("part 2:", absolute_minimum_location_number) # finally done at 21:43

