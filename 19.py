import fileinput
# this one looks like a firewall
from sys import exit

workflows = {}
parts = []
reading_workflows = True

always_match = lambda q: True

for line in fileinput.input():
    line = line.rstrip()
    if len(line) == 0:
        reading_workflows = False
        continue
    if reading_workflows:
        line = line.rstrip("}")
        label, rulestring = line.split("{")
        rulestrings = rulestring.split(",")
        rules = []
        for rule in rulestrings:
            if ":" not in rule:
                rules.append((None, None, None, rule))
                continue
            ruletext, destination = rule.split(":")
            property_index = "xmas".index(ruletext[0])
            assert ruletext[1] in "<>"
            val = int(ruletext[2:])
            rules.append((property_index, ruletext[1], val, destination))
        workflows[label] = rules
    else:
        components = line.strip("{}").split(",")
        quadruplet = tuple(map(lambda s: int(s[2:]), components))
        parts.append(quadruplet)

def apply_workflow(part, cur_label):
    global workflows
    rules = workflows[cur_label]
    for (property_index, op_symbol, value, destination) in rules:
        if property_index == None:
            return destination
        if op_symbol == "<" and part[property_index] < value:
            return destination
        elif op_symbol == ">" and part[property_index] > value:
            return destination
    raise Exception(f"part {part} with label {label} didn't go anywhere")

def is_part_accepted(part):
    label = "in"
    while label not in ("A", "R"):
        label = apply_workflow(part, label)
    return label == "A"

accepted_parts = filter(is_part_accepted, parts)
print("part 1:", sum(map(sum, accepted_parts))) # 373302
exit(0)

