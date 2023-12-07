import fileinput
from functools import cmp_to_key
card_labels = "23456789TJQKA"
card_labels_part_2 = "J23456789TQKA"

def categorize_hand(hand_str):
    label_occurrences = {}
    for card_label in hand_str:
        if card_label not in label_occurrences:
            label_occurrences[card_label] = 0
        label_occurrences[card_label] += 1
    occurrence_nums = list(sorted(label_occurrences.values(), reverse=True))
    #print(hand_str, label_occurrences, occurrence_nums)
    if len(label_occurrences) == 1 and occurrence_nums == [5]:
        return 5 # five of a kind
    elif len(label_occurrences) == 2:
        if occurrence_nums == [4, 1]:
            return 4 # four of a kind
        elif occurrence_nums == [3, 2]:
            return 3.5 # full house
        else:
            return 0.3 # this shouldn't happen with well-formed inputs
    elif len(label_occurrences) == 3:
        if occurrence_nums == [3, 1, 1]:
            return 3 # three of a kind
        elif occurrence_nums == [2, 2, 1]:
            return 2 # two pair
        else:
            return 0.2 # this shouldn't happen with well-formed inputs
    elif len(label_occurrences) == 4 and occurrence_nums == [2, 1, 1, 1]:
        return 1.5 # one pair
    elif len(label_occurrences) == 5 and occurrence_nums == [1, 1, 1, 1, 1]:
        return 1 # high card
    return 0.1 # this shouldn't happen with well-formed inputs

def categorize_hand_part_2(hand_str):
    label_occurrences = {}
    for card_label in hand_str:
        if card_label not in label_occurrences:
            label_occurrences[card_label] = 0
        label_occurrences[card_label] += 1
    occurrence_nums = list(sorted(label_occurrences.values(), reverse=True))
    #print(hand_str, label_occurrences, occurrence_nums)
    if len(label_occurrences) == 1 and occurrence_nums == [5]:
        return 5 # five of a kind
    elif len(label_occurrences) == 2:
        if occurrence_nums == [4, 1]:
            if "J" in label_occurrences:
                return 5 # either a JJJJX or XXXXJ, but still a five of a kind
            return 4 # four of a kind
        elif occurrence_nums == [3, 2]:
            if "J" in label_occurrences:
                return 5 # either XXJJJ or XXXJJ, five of a kind in any case
            return 3.5 # full house
        else:
            return 0.3 # this shouldn't happen with well-formed inputs
    elif len(label_occurrences) == 3:
        if occurrence_nums == [3, 1, 1]:
            if "J" in label_occurrences:
                if label_occurrences["J"] == 1:
                    return 4 # it's a XXXYJ four of a kind
                elif label_occurrences["J"] == 3:
                    return 4 # still a four of a kind, just XYJJJ
            return 3 # three of a kind
        elif occurrence_nums == [2, 2, 1]:
            if "J" in label_occurrences:
                if label_occurrences["J"] == 1:
                    return 3.5 # XXYYJ -> XXYYY, full house
                else:
                    return 4 # XXYJJ -> XXYXX, four of a kind
            return 2 # two pair
        else:
            return 0.2 # this shouldn't happen with well-formed inputs
    elif len(label_occurrences) == 4 and occurrence_nums == [2, 1, 1, 1]:
        if "J" in label_occurrences:
            return 3 # three of a kind: either XYZJJ -> XYZZZ, or XXYZJ -> XXYZX
        return 1.5 # one pair
    elif len(label_occurrences) == 5 and occurrence_nums == [1, 1, 1, 1, 1]:
        if "J" in label_occurrences:
            return 1.5 # one pair: XYZWJ -> XYZWX
        return 1 # high card
    return 0.1 # this shouldn't happen with well-formed inputs

# +1: a beats b, -1: b beats a, 0: tied
# idk if this is the conventional way to integerify order or if it's the opposite
def compare_hands(a, b, part_1 = True):
    if part_1:
        a_cat = categorize_hand(a)
        b_cat = categorize_hand(b)
    else:
        a_cat = categorize_hand_part_2(a)
        b_cat = categorize_hand_part_2(b)
    if a_cat < b_cat:
        return -1
    elif a_cat > b_cat:
        return 1
    else:
        for i in range(0, 5):
            if part_1:
                a_val = card_labels.find(a[i])
                b_val = card_labels.find(b[i])
            else:
                a_val = card_labels_part_2.find(a[i])
                b_val = card_labels_part_2.find(b[i])
            if a_val < b_val:
                return -1
            elif a_val > b_val:
                return 1
    return 0

def compare_hand_bid_pairs_part_1(a, b):
    return compare_hands(a[0], b[0], part_1 = True)

def compare_hand_bid_pairs_part_2(a, b):
    return compare_hands(a[0], b[0], part_1 = False)

compare_hand_bid_pairs_key = cmp_to_key(compare_hand_bid_pairs_part_1)
compare_hand_bid_pairs_key_pt2 = cmp_to_key(compare_hand_bid_pairs_part_2)

hands_bids = []
for line in fileinput.input():
    line_parts = line.rstrip().split()
    hand = line_parts[0]
    hands_bids.append((hand, int(line_parts[1])))
#print(hands_bids)
#print("---")
sorted_bids = zip(sorted(hands_bids, key=compare_hand_bid_pairs_key), range(1, len(hands_bids)+1))
# after the zip, our array elements are nested tuples: ((hand, bid), rank).
# we're only interested in bid * rank, disregard hand.
rank_multiplier = lambda tup: tup[0][1] * tup[1]
winnings = map(rank_multiplier, sorted_bids)
print("part 1:", sum(winnings)) # done at 07:34

#print(*sorted(hands_bids, key=compare_hand_bid_pairs_key_pt2))
sorted_bids_pt2 = zip(sorted(hands_bids, key=compare_hand_bid_pairs_key_pt2), range(1, len(hands_bids)+1))
winnings_pt2 = map(rank_multiplier, sorted_bids_pt2)
print("part 2:", sum(winnings_pt2)) # done at 07:52
print()
