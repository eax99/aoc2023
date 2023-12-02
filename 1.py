import fileinput

# ugly implementation: there's unnecessary splitting-up and rebuilding of
# strings, but it's the first thing that came to mind and it works.

def fixline(s):
    # the part two thing
    n = len(s)
    sbuf = []
    i = 0
    while i < n:
        if s[i] == 'o':
            if i < n - 2 and s[i+1] == 'n' and s[i+2] == 'e':
                sbuf.append('1')
            else:
                sbuf.append(s[i])
        elif s[i] == 't':
            if i < n - 2 and s[i+1] == 'w' and s[i+2] == 'o':
                sbuf.append('2')
            elif i < n - 4 and s[i+1] == 'h' and s[i+2] == 'r' and s[i+3] == 'e' and s[i+4] == 'e':
                sbuf.append('3')
            else:
                sbuf.append(s[i])
        elif s[i] == 'f' and i < n - 3:
            if s[i+1] == 'o' and s[i+2] == 'u' and s[i+3] == 'r':
                sbuf.append('4')
            elif s[i+1] == 'i' and s[i+2] == 'v' and s[i+3] == 'e':
                sbuf.append('5')
            else:
                sbuf.append(s[i])
        elif s[i] == 's':
            if i < n-2 and s[i+1] == 'i' and s[i+2] == 'x':
                sbuf.append('6')
            elif i < n-4 and s[i+1] == 'e' and s[i+2] == 'v' and s[i+3] == 'e' and s[i+4] == 'n':
                sbuf.append('7')
            else:
                sbuf.append(s[i])
        elif s[i] == 'e':
            if i < n-4 and s[i+1] == 'i' and s[i+2] == 'g' and s[i+3] == 'h' and s[i+4] == 't':
                sbuf.append('8')
            else:
                sbuf.append(s[i])
        elif s[i] == 'n':
            if i < n-3 and s[i+1] == 'i' and s[i+2] == 'n' and s[i+3] == 'e':
                sbuf.append('9')
            else:
                sbuf.append(s[i])
        else:
            sbuf.append(s[i])
        i += 1
    return "".join(sbuf)

total = 0
for line in fileinput.input():
    line = fixline(line) # comment out to compute part 1
    firstnum = None
    lastnum = None
    for char in line:
        if firstnum == None and char in "0123456789":
            firstnum = char
            lastnum = char
        elif char in "0123456789":
            lastnum = char
    number = int(firstnum) * 10 + int(lastnum)
    total += number
print(total)
# part 2 done at 07:49 (utc+2), third place in our private leaderboard :D
