import fileinput
from math import ceil
from operator import mul
from functools import reduce
times = []
distances = []
line1 = True
for line in fileinput.input():
    line = line.rstrip()
    parts = line.split()
    numbers = list(map(int, parts[1:]))
    if line1:
        times = numbers
        line1 = False
    else:
        distances = numbers
races = list(zip(times, distances))

wins_per_race = []
for (time, distance_record) in races:
    ways_to_win = 0
    for button_holding_time in range(0, time + 1):
        speed = button_holding_time
        remaining_time = time - button_holding_time
        my_boats_distance = speed * remaining_time
        if my_boats_distance > distance_record:
            ways_to_win += 1
    wins_per_race.append(ways_to_win)
product = reduce(mul, wins_per_race, 1)
print(wins_per_race)
print("part 1:", product) # done at 07:25, with a start at 07:12
print()

# part 2, with much more interesting math
part_2_time = ''.join(map(str, times))
part_2_distance = ''.join(map(str, distances))
print(part_2_time, part_2_distance)
