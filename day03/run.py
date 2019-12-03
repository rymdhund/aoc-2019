def read():
    with open("input") as f:
        a, b, _ = f.read().split("\n")
        return a.split(","), b.split(",")

def dist(p):
    return abs(p[0]) + abs(p[1])

def make_path(steps):
    path = {}
    x = 0
    y = 0
    i = 1
    for step in steps:
        d = step[0]
        dist = int(step[1:])
        dx, dy = 0, 0
        if d == "R":
            dx = 1
        elif d == "L":
            dx = -1
        elif d == "U":
            dy = 1
        elif d == "D":
            dy = -1

        for _ in range(dist):
            x += dx
            y += dy
            if (x, y) not in path:
                path[(x, y)] = i
            i += 1

    return path

def closest_cross_manhattan(steps1, steps2):
    set1 = set(make_path(steps1).keys())
    set2 = set(make_path(steps2).keys())
    crosses = set1.intersection(set2)
    best = sorted(crosses, key=dist)[0]
    return dist(best)

def closest_cross_steps(steps1, steps2):
    path1 = make_path(steps1)
    path2 = make_path(steps2)
    set1 = set(path1.keys())
    set2 = set(path2.keys())
    crosses = set1.intersection(set2)
    best = sorted(crosses, key=lambda pos: path1[pos] + path2[pos])[0]
    return path1[best] + path2[best]

def solve1():
    steps1, steps2 = read()
    print(closest_cross_manhattan(steps1, steps2))

def solve2():
    steps1, steps2 = read()
    print(closest_cross_steps(steps1, steps2))

solve1()
solve2()
