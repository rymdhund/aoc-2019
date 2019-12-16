from typing import Tuple, List, Dict
from dataclasses import dataclass
import math

AU = Tuple[int, str]

@dataclass
class Reaction:
    amount: int
    sources: List[AU]

def parse(s):
    def au(x):
        a, b = x.split(" ")
        return int(a), b

    reactions = {}
    for line in s.split("\n"):
        if not line:
            continue

        a, b = line.split(" => ")
        sources = [
            au(m) for m in a.split(", ")
        ]
        amount, unit = au(b)
        reactions[unit] = Reaction(amount, sources)

    return reactions


def step(r, need):
    for unit, amount in need.items():
        if amount <= 0 or unit == "ORE":
            continue

        reaction = r[unit]
        mult = math.ceil(amount/reaction.amount)
        need[unit] -= reaction.amount * mult
        for a, u in reaction.sources:
            need[u] = need.get(u, 0) + a*mult
        return True
    return False

def ore(r, fuel):
    need = {"FUEL": fuel}
    while step(r, need):
        pass
    return need["ORE"]


def solve1():
    with open("input") as f:
        s = f.read()
    r = parse(s)
    print(ore(r, 1))


def solve2():
    with open("input") as f:
        s = f.read()
    r = parse(s)

    big_step = 10000
    fuel = 1
    while ore(r, fuel + big_step) < 1000000000000:
        fuel += big_step

    while ore(r, fuel+1) < 1000000000000:
        fuel += 1

    print(fuel)

solve1()
solve2()
