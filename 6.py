import fileinput
from math import ceil, comb
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
    ways_to_lose = 0 + (distance_record / time)
    for button_holding_time in range(0, time):
        speed = button_holding_time
        remaining_time = time - button_holding_time
        my_boats_distance = speed * remaining_time
        my_boats_distance_2 = button_holding_time * (time - button_holding_time)
        #print(time, distance_record, button_holding_time, my_boats_distance, my_boats_distance > distance_record)
        if my_boats_distance > distance_record:
            ways_to_win += 1
    wins_per_race.append(ways_to_win)
    #print(ways_to_win, ways_to_lose)
    #print()
product = reduce(mul, wins_per_race, 1)
print(wins_per_race)
print("part 1:", product) # done at 07:25, with a start at 07:12
print()

# part 2, with much more interesting math
part_2_time = int(''.join(map(str, times)))
part_2_distance = int(''.join(map(str, distances)))
print(part_2_time, part_2_distance)

part_2 = 0
for button_holding_time in range(0, part_2_time):
    #if button_holding_time & (2**20-1) == 0:
    #    print(".", end="", flush=True) # progress bar
    speed = button_holding_time
    remaining_time = part_2_time - button_holding_time
    my_boats_distance = speed * remaining_time
    #my_boats_distance = button_holding_time * (time - button_holding_time)
    if my_boats_distance > part_2_distance:
        part_2 += 1
print("\npart 2:", part_2) # 08:16
# surprisingly brute-forcing wasn't that slow (45 sec),
# still wish i found the elegant answer though
