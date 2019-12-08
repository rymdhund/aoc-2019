# coding: utf8

def layers(data, h, w):
    ls = []
    for i in range(0, len(data), h*w):
        ls.append([int(c) for c in data[i:i+h*w]])
    return ls

def read_layers():
    with open("input") as f:
        s = f.read().strip()

    return layers(s, 25, 6)

def count(l, d):
    return sum(1 for x in l if x == d)

def solve1():
    def zeroes(l):
        return sum(1 for d in l if d == 0)

    ls = read_layers()

    min_0 = sorted(ls, key=zeroes)[0]
    print(count(min_0, 1) * count(min_0, 2))

def solve2():
    def d_to_c(d):
        return "█" if d == 0 else " "

    ls = read_layers()

    img = [2] * (25*6)

    for l in ls:
        for i, d in enumerate(img):
            if d == 2:
                img[i] = l[i]

    for i in range(6):
        print("".join(d_to_c(d) for d in img[i*25:i*25+25]))


solve1()
solve2()
