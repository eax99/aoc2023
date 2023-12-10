import fileinput
# this week: the difference engine! newton's method of divided differences.
histories = []
for line in fileinput.input():
    line = line.rstrip()
    histories.append(list(map(int, line.split())))

def get_differences(array):
    differences = []
    for i in range(len(array) - 1):
        differences.append(array[i+1] - array[i])
    return differences

def all_zero(array):
    for n in array:
        if n != 0:
            return False
    return True

def get_difference_tableau(history):
    diff = get_differences(history)
    all_differences = [history, diff]
    while not all_zero(diff):
        diff = get_differences(diff)
        all_differences.append(diff)
    return all_differences

def predict(history):
    all_differences = get_difference_tableau(history)
    next_val_up = 0
    for numrow in reversed(all_differences[:-1]): # skip the all-zeros final one
        next_val_up = numrow[-1] + next_val_up
    return next_val_up

def predict_backwards(history):
    all_differences = get_difference_tableau(history)
    next_val_down = 0
    for numrow in reversed(all_differences[:-1]):
        next_val_down = numrow[0] - next_val_down
        #print(next_val_down, numrow)
    return next_val_down

extrapolated_values = []
backward_extrapolated_values = []
for history in histories:
    extrapolated_values.append(predict(history))
    backward_extrapolated_values.append(predict_backwards(history))
    #print(predict_backwards(history))
print("part 1:", sum(extrapolated_values)) # 07:17 UTC+2
print("part 2:", sum(backward_extrapolated_values)) # 07:24 UTC+2
print()
