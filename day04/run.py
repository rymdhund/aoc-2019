def valid(pw):
    same = False
    last = None
    for i in range(6):
        d = (pw // (10 ** i)) % 10

        if last != None and last == d:
            same = True

        if last != None and last < d:
            return False

        last = d

    return same

def valid2(pw):
    pair = False
    l1, l2, l3 = None, None, None
    for i in range(6):
        d = (pw // (10 ** i)) % 10

        if l1 is not None and d != l1 and l1 == l2 and l2 != l3:
            pair = True 

        if l1 is not None and l1 < d:
            return False

        l3, l2, l1 = l2, l1, d

    if l1 == l2 and l2 != l3:
        pair = True

    return pair 


sol1 = sum(1 for pw in range(240298, 784956) if valid(pw))
print(sol1)

sol2 = sum(1 for pw in range(240298, 784956) if valid2(pw))
print(sol2)
