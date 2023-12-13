import fileinput
import re
import time
instances = []
for line in fileinput.input():
    line = line.rstrip()
    parts = line.split()
    numberlist = list(map(int, parts[1].split(",")))
    instances.append((parts[0], numberlist))

dbg = False

def numericize_text(text):
    run_length = 0
    prev_char = None
    run_lengths = []
    # the extra null character is so we also get the final run-length pair;
    # it's a way to force an extra iteration, and it'll never occur in the
    # text itself (i checked) so it can't contaminate the run lengths.
    for char in text + "\0":
        if char == prev_char:
            run_length += 1
        else:
            if prev_char != None:
                run_lengths.append((prev_char, run_length))
            run_length = 1
            prev_char = char
    return run_lengths

def could_fit():
    pass

# upper level: take in the problem-assigned text, split it up into
# components, and pass it to the lower level. components are separated
# by a run of dots.
def count_arrangements_1(text, numbers):
    period_separated_bits_with_possible_empty_strings = re.split(r'\.+', text)
    period_separated_bits = list(filter(lambda s: len(s) > 0,
                    period_separated_bits_with_possible_empty_strings))
    # the period_separated_bits consist only of '#'s and '?'s
    if dbg: print(text, period_separated_bits, " ".join(map(str, numbers)))
    #count_arrangements(period_separated_bits, numbers)
    n = starting_index_analysis(text, numbers)
    if dbg: print(text, "->", n)
    return n

# prefix is just used for debug printing
def starting_index_analysis(text, numbers, prefix=''):
    # with this approach, we look at the numbers first, and the string of
    # octothorpes that each number represents:
    # starting from the left, where could they start?
    # if they start here, could the rest of the numbers fit?
    # in how many ways could the rest of the numbers fit?
    # this is a recursive function; each iteration will consume a number off
    # the front, split the text at some point, but not increment a counter
    # itself; only with one number remaining will actual counting happen.
    first_number = numbers[0]
    other_numbers = numbers[1:]
    possible_ways = 0
    for i in range(len(text)):
        if text[i] in ('?', '#'):
            # this is a valid starting position for some number --
            # what about ours, which is the first of the list?
            if i > 0 and '#' in text[:i]:
                # we're past the starting position of the first number
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because there's a '#' behind it")
                break
            if first_number > len(text) - i:
                # can't start here -- too close to the end
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because it's too near the end")
                break
            if i + first_number <= len(text) and '.' in text[i:i+first_number]:
                # can't start here -- there's a '.' where we need a '#' or '?'
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because there's a '.' in the way")
                continue
            if i + first_number < len(text) and text[i + first_number] == '#':
                # can't start here -- there's a '#' where we would need a '.'
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because of the '#' at index", i + first_number)
                #text = ('.' * (i - 1)) + text[i:]
                continue

            # the extra +1 is for the dot that must separate this number from the rest
            text_required_for_remaining_numbers = sum(other_numbers) + len(other_numbers) - 1 + 1
            if text_required_for_remaining_numbers > len(text) - i:
                # can't start here -- we can't fit the rest
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because", other_numbers, "can't fit in", len(text) - i, "chars")
                break

            # now look at the components of the remaining text,
            # components being runs of /[#?]+/ separated by /.+/.
            # (splitting is in two steps to remove empty strings)
            components_ = re.split(r'\.+', text[i+first_number+1:])
            components = list(filter(lambda s: len(s) > 0, components_))
            #print(repr(text), first_number, "remaining components:", components)
            # we can fit [2] into ['?', '??#'], but not into ['#', '??#']
            numbers_needed = len(list(filter(lambda s: '#' in s, components)))
            if len(other_numbers) < numbers_needed:
                if dbg: print(repr(prefix+text), first_number, "cannot start at", i, "because", other_numbers, "can't fit in the text", text[i+first_number+1:])
                # this continue is critical: if it's turned into a break
                # this routine will under-count. this makes sense:
                # other_numbers could be [], and in the case where there's
                # only one remaining '#', we need to keep iterating until
                # we find it and make first_number contain it.
                continue

            #print(repr(prefix + text), first_number, "could start at index", i)
            if dbg: print(repr(prefix + text[:i] + ('#' * first_number) + '.' + text[i + first_number + 1:]), first_number, "could start at index", i)

            # now that we know that this number can start here, recurse.
            # or don't recurse if there's nothing to recurse to,
            # but increment a counter instead.
            if len(other_numbers) > 0:
                # (virtually) add a '.' after our run of '#'s
                remaining_text = text[i + first_number + 1:]
                debug_print_prefix = prefix + ' '*i + '-'*first_number + ' '
                n = starting_index_analysis(remaining_text, tuple(other_numbers), prefix = debug_print_prefix)
                if dbg: print(repr(prefix + text[:i] + ('#' * first_number) + '.' + text[i + first_number + 1:]), first_number, "starting at index", i, "ended up with", n, "possible ways")
                possible_ways += n
            else:
                possible_ways += 1
#        else:
#            print(repr(text), first_number, "can't start at", i, "because it's a '.'")
    return possible_ways

# lower level: take in a list of text components and a list of numbers,
# then try fitting those numbers to those text components.
def count_arrangements(text_components, numbers):
    # dividing the problem:
    # if there are any runs of '#'s on their own, we can use this to
    # pin down some of the numbers. we can then run a more complicated
    # counting procedure on the remaining parts. there may, of course, be
    # multiple ways of pinning down the number list... so we'll run the
    # complicated counting procedure on each of those ways, and if one
    # of the ways ends up providing an invalid assignment (the character
    # assignments don't match the number list) then we ignore those results.
    #
    # what we do exactly is that we 
    for (index_of_bit, textbit) in enumerate(text_components):
        if '?' not in textbit:
            # this textbit contains only '#'s.
            octothorpe_run_length = len(textbit)
            components_before = text_components[0:index_of_bit]
            components_after = text_components[index_of_bit + 1:]
            # we're interested in not only how many total assignable
            # characters there are in the components before/after this run of
            # octothorpes, but how many separate components there are;
            # we can't assign [1, 2] into '???', but we could assign it to
            # ['?', '??#'] or ['?#', '??'].
            text_available_before = len(' '.join(components_before))
            text_available_after = len(' '.join(components_after))
            # other measures that we use to prune out invalid assignments. 
            longest_available_before = max(map(len, components_before), default=0)
            longest_available_after = max(map(len, components_after), default=0)
            # these numbers will tell us the minimum number of numbers
            # we can try assigning to either side: we can assign [2] to
            # ['?', '??#'], but we can't assign it to ['#', '??#'].
            numbers_needed_before = len(list(filter(lambda s: '#' in s, components_before)))
            numbers_needed_after = len(list(filter(lambda s: '#' in s, components_after)))
            #length_of_bits_before = sum(map(len, components_before))
            #length_of_bits_after = sum(map(len, components_after))
            # find out whether dividing the problem at some number N could
            # work: can we fit the numbers before N into the text bits
            # before this one, and the ones after N into the text bits
            # after this one?
            for (index_of_num, num) in enumerate(numbers):
                if num != octothorpe_run_length:
                    continue
                else:
                    numbers_before = numbers[0:index_of_num]
                    numbers_after = numbers[index_of_num + 1:]
                    # take into account that we need to separate octothorpes
                    # with one or more dots.
                    text_length_needed_before = sum(numbers_before) + len(numbers_before) - 1
                    text_length_needed_after = sum(numbers_after) + len(numbers_after) - 1
                    if text_length_needed_before > text_available_before:
                        continue
                    if text_length_needed_after > text_available_after:
                        continue
                    if len(numbers_before) < numbers_needed_before:
                        print("skipping assignment of", components_before, textbit, components_after, ": can't fit", numbers_before, "into", components_before)
                        continue
                    if len(numbers_after) < numbers_needed_after:
                        print("skipping assignment of", components_before, textbit, components_after, ": can't fit", numbers_after, "into", components_after)
                        continue
                    # it's worth investigating further.
                    # we will recurse on the first pinning-down of the #
                    # to avoid double-counting.
                    print(components_before, textbit, components_after, ":", numbers_before, "into", components_before, ";", numbers_after, "into", components_after)
#            print(textbits_before, length_of_bits_before, index_of_bit, octothorpe_run_length, length_of_bits_after, textbits_after)
    print()




total_arrangements_pt1 = 0
for (text, numbers) in instances:
    total_arrangements_pt1 += count_arrangements_1(text, numbers)

print("part 1:", total_arrangements_pt1)
# part 2 is intractable with the current sort-of-brute-force recursive algorithm

total_arrangements_pt2 = 0
#prev_time = time.time()
for (i, (text, numbers)) in enumerate(instances):
    continue
    megatext = text + '?' + text + '?' + text + '?' + text + '?' + text
    meganumbers = numbers * 5
    #print(text, megatext, sep="\n")
    #print(numbers, meganumbers, sep="\n")
    total_arrangements_pt2 += count_arrangements_1(megatext, meganumbers)
#    if i % 1 == 0:
#        now = time.time()
#        timedelta = now - prev_time
#        estimate = (len(instances) - i - 1) * timedelta
#        prev_time = now
#        print(i, total_arrangements_pt2, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), f'{timedelta:.01f} sec for 1, {estimate:.01f} sec for remaining {len(instances) - i - 1}')

#print("part 2:", total_arrangements_pt2)
print()

    # recalling regular expressions in the classical sense.
    # forming a representation of what a valid string _could_ look like,
    # then fitting the given string to that representation.

    # disregard the above.

                    # we need to avoid double counting: cases like the text
                    # having '[...].#.#.[...]' and the numbers having
                    # [..., 1, 1, 1, ...] are tricky.
