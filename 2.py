import fileinput
linenumber = 0
passing_games = [] # part 1
power_sum = 0 # part 2
for line in fileinput.input():
    linenumber += 1
    minimum_cubes_needed = {"red": 0, "green": 0, "blue": 0}
    line = line.rstrip() # trailing newline
    id_part, sample_part = line.split(": ")
    samplings = sample_part.split("; ")
    for sampling in samplings:
        for sample in sampling.split(", "):
            number, name = sample.split(" ")
            if minimum_cubes_needed[name] < int(number):
                minimum_cubes_needed[name] = int(number)
    # part 1
    if minimum_cubes_needed["red"] <= 12 and minimum_cubes_needed["green"] <= 13 and minimum_cubes_needed["blue"] <= 14:
        passing_games.append(linenumber)
    # part 2
    game_power = minimum_cubes_needed["red"] * minimum_cubes_needed["green"] * minimum_cubes_needed["blue"]
    power_sum += game_power

print("part 1:", sum(passing_games))
print("part 2:", power_sum)
# part 2 finished at 07:16 UTC+2
