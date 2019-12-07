def make_map(s):
    m = {}
    for orb in s.split("\n"):
        if orb:
            a, b = orb.split(")")
            m.setdefault(a, []).append(b)
    return m


def count_children(m, base):
    if base not in m:
        return 0

    cnt = 0
    for child in m[base]:
        cnt += count_children(m, child) + 1
    return cnt


def count_orbits(m, base):
    s = count_children(m, base)
    if s == 0:
        return 0
    for child in m[base]:
        s += count_orbits(m, child)

    return s

def distance_to(m, base, node):
    if base == node:
        return 0

    if base not in m:
        return None

    for child in m[base]:
        d = distance_to(m, child, node)
        if d != None:
            return d + 1


def santa_you_dist(m, node):
    sd = distance_to(m, node, "SAN")
    if sd is None:
        return None
    yd = distance_to(m, node, "YOU")
    if yd is None:
        return None
    return sd + yd


def min_you_san(m):
    mi = 100000
    for k in m.keys():
        syd = santa_you_dist(m, k)
        if syd is not None and syd < mi:
            mi = syd
    return mi


def solve():
    with open("input") as f:
        m = make_map(f.read())
    print(count_orbits(m, "COM"))

    print(min_you_san(m)-2)

solve()
