import fileinput
special_symbols = "#$%&*+-/=@"
#chararray = []
symbol_locs = []
symbols_by_loc = {}
asterisk_positions = []
numbers_and_locs = [] # tuples of number, line, pos of first char, pos of last char
linenumber = 0
for line in fileinput.input():
    line = line.rstrip()
    #chararray.append(list(line))
    numbuffer = []
    num_start = -1
    num_end = -1
    for (n, char) in enumerate(line):
        if char == ".":
            if len(numbuffer) > 0: # first non-digit after a number
                num_end = num_start + len(numbuffer) - 1
                number = int("".join(numbuffer))
                numbers_and_locs.append((number, linenumber, num_start, num_end))
                numbuffer, num_start, num_end = [], -1, -1
        elif char in "0123456789":
            if len(numbuffer) == 0: # first digit of a new number
                num_start = n
            numbuffer.append(char)
        else:
            if char not in "0123456789.":
                symbol_locs.append((linenumber, n))
                symbols_by_loc[(linenumber, n)] = char
                if char == '*':
                    asterisk_positions.append((linenumber, n))
            if len(numbuffer) > 0: # first non-digit after a number
                num_end = num_start + len(numbuffer) - 1
                number = int("".join(numbuffer))
                numbers_and_locs.append((number, linenumber, num_start, num_end))
                numbuffer, num_start, num_end = [], -1, -1
    if len(numbuffer) > 0:
        num_end = num_start + len(numbuffer) - 1
        number = int("".join(numbuffer))
        numbers_and_locs.append((number, linenumber, num_start, num_end))
        numbuffer, num_start, num_end = [], -1, -1
    linenumber += 1
#print(symbol_locs)
#print(symbols_by_loc)
print()
print(*numbers_and_locs, sep="\n")
print()
print('*:', asterisk_positions)
partnumbers = []
numbers_by_loc = {}
distinguisher = 1
for (number, linenumber, firstcharpos, lastcharpos) in numbers_and_locs:
    # part 2
    for possible_column in range(firstcharpos, lastcharpos + 1):
        numbers_by_loc[(linenumber, possible_column)] = (number, distinguisher)
    distinguisher += 1
    # part 1
    num_digits = len(str(number))
    possible_symbol_locs = []
    for possible_row in range(linenumber - 1, linenumber + 2):
        for possible_col in range(firstcharpos - 1, lastcharpos + 2):
            if possible_row >= 0 and possible_col >= 0 and not (possible_row == linenumber and possible_col in range(firstcharpos, lastcharpos + 1)):
                possible_symbol_locs.append((possible_row, possible_col))
    #print(number, possible_symbol_locs)
    for look_position in possible_symbol_locs:
        if look_position in symbol_locs:
            partnumbers.append(number)
            #print(number, look_position, symbols_by_loc[look_position])
            break
#for (linenum, line) in enumerate(chararray):
#    digit_counter = 0
#   for (charnum, char) in enumerate(line):
#       if digit_counter == 0:
#            pass

#print(*chararray, sep="\n")
#print('parts:', partnumbers)
print("part 1:", sum(partnumbers))
gear_ratios = []
for (star_row, star_col) in asterisk_positions:
    looked_up_numbers = []
    for lookup_row in range(star_row - 1, star_row + 2):
        for lookup_col in range(star_col - 1, star_col + 2):
            if (lookup_row, lookup_col) in numbers_by_loc:
                number_with_distinguisher = numbers_by_loc[(lookup_row, lookup_col)]
                if number_with_distinguisher not in looked_up_numbers:
                    looked_up_numbers.append(number_with_distinguisher)
    print(f"star at {star_row},{star_col}:", looked_up_numbers)
    if len(looked_up_numbers) == 2:
        gear_ratio = looked_up_numbers[0][0] * looked_up_numbers[1][0]
        gear_ratios.append(gear_ratio)
        print(f"star at {star_row},{star_col} has ratio", gear_ratio)
print("part 2:", sum(gear_ratios))
print()
# part 2 completed at 07:59 UTC+2
