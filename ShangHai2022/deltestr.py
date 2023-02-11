s = input("")
def deleteStr(s):
    indexList = []
    for x in (1, len(s)-2):
        if (s[x]==s[x-1] and s[x]!=s[x+1]) or (s[x]!=s[x-1] and s[x]==s[x+1]):
            indexList.append(x)
    for i in indexList:
        s = s.replace(s[i], "", 1)
    return s

for p in range(0, pow(2, 64)):
    if s == "":
        break
    else:
        s = deleteStr(s)

if s == "":
    print('empty')
else:
    print(s)