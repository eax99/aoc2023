import fileinput
totalpoints = 0
matches_by_card = {}
copies = {}
for line in fileinput.input():
    line = line.rstrip()
    id_part, other_part = line.split(": ")
    card_id = int(id_part.split()[1])
    copies[card_id] = 1
    left_part, right_part = other_part.split(" | ")
    winningnums = set(map(int, left_part.split()))
    nums_i_have = set(map(int, right_part.split()))
    matches = len(nums_i_have & winningnums)
    matches_by_card[card_id] = matches
    points = 0
    if matches > 0:
        points = 2 ** (matches - 1)
    totalpoints += points

print("part 1:", totalpoints) # part 1 done at 07:07 UTC+2

for card_id in matches_by_card:
    num_matches = matches_by_card[card_id]
    num_card_copies = copies[card_id]
    for i in range(num_matches):
        copies[card_id + i + 1] += num_card_copies

print("part 2:", sum(copies.values())) # part 2 done at 07:17 UTC+2

