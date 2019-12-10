import math


def simplify(x, y):
    # Quick and dirty gcf
    ax, ay = abs(x), abs(y)
    if ax == 0:
        return 0, y//ay
    if ay == 0:
        return x//ax, 0

    for n in range(2, min(ax, ay)+1):
        if x % n == 0 and y % n == 0:
            return simplify(x // n, y // n)

    return x, y


def get_line(src, dest):
    """
    return a line of sight
    direction is important and 1, 0 is different from -1,0
    """
    ax, ay = src
    bx, by = dest
    dx, dy = bx-ax, by-ay
    return simplify(dx, dy)


def group_by_line(base, coords):
    lines = {}
    for c in coords:
        if c != base:
            line = get_line(base, c)
            lines.setdefault(line, []).append(c)
    return lines


def num_lines(base, coords):
    return len(group_by_line(base, coords))


def angle(line):
    # return the clockwise angle of a line, starting straight up
    v = math.pi/2 - math.atan2(-line[1], line[0])
    return v % (2*math.pi)


def parse(s):
    coords = []
    for y, l in enumerate(s.split("\n")):
        for x, c in enumerate(l):
            if c == "#":
                coords.append((x, y))
    return coords


def solve1(s):
    m = parse(s)
    res = max(num_lines(base, m) for base in m)
    return res


def solve2(s):
    m = parse(s)
    def order(b):
        return num_lines(b, m)
    best = sorted(m, key=order, reverse=True)[0]

    lines = group_by_line(best, m)
    ordered_lines = sorted(lines.keys(), key=angle)

    def dist_to_best(c):
        return abs(c[0]-best[0]) + abs(c[1]-best[1])

    i = 0
    while i < 200:
        idx = ordered_lines[i % len(ordered_lines)]
        coords = lines[idx]
        if coords:
            closest = sorted(coords, key=dist_to_best)[0]
            coords.remove(closest)
            i += 1

    return closest[0]*100 + closest[1]

def main():
    with open("input") as f:
        print(solve1(f.read()))

    with open("input") as f:
        print(solve2(f.read()))


main()
