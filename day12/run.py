from typing import Tuple
from dataclasses import dataclass

@dataclass
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, o):
        return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)

    @staticmethod
    def _d(v):
        if v < 0:
            return -1
        if v > 0:
            return 1
        return 0

    def delta(self, o):
        return Vec3(self._d(o.x-self.x), self._d(o.y-self.y), self._d(o.z-self.z))

    def abs(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

@dataclass
class Moon:
    pos: Vec3
    vel: Vec3

    def energy(self):
        return self.pos.abs() * self.vel.abs()

def apply_gravity(moons):
    for moon1 in moons:
        for moon2 in moons:
            if moon1 == moon2:
                continue
            gravity = moon1.pos.delta(moon2.pos)
            moon1.vel += gravity

def apply_velocity(moons):
    for moon in moons:
        moon.pos += moon.vel

def step(moons):
    apply_gravity(moons)
    apply_velocity(moons)


def parse(s):
    moons = []
    for line in s.split("\n"):
        if line:
            cs = line.strip("<>").split(", ")
            coord = tuple(int(v.lstrip("xyz=")) for v in cs)
            pos = Vec3(coord[0], coord[1], coord[2])
            moons.append(Moon(pos, Vec3(0, 0, 0)))
    return moons

def tot_energy(moons):
    return sum(m.energy() for m in moons)

def solve1():
    with open("input") as f:
        s = f.read()
    moons = parse(s)
    for i in range(1000):
        step(moons)
    print(sum(m.energy() for m in moons))

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def step_pv(ps, vs):
    for i in range(4):
        for j in range(i+1, 4):
            if ps[i] < ps[j]:
                vs[i] += 1
                vs[j] -= 1
            elif ps[i] > ps[j]:
                vs[i] -= 1
                vs[j] += 1
    for i in range(4):
        ps[i] += vs[i]

def find_cycle(positions):
    """
    Calculate the length of a cycle for one dimension
    """
    ps = positions[:]
    vs = [0,0,0,0]

    goal = positions, vs[:]
    i = 0
    while True:
        step_pv(ps, vs)
        i += 1
        if (ps,vs) == goal:
            break

    return i

def solve2():
    """
    1) We can look at the x, y, z coordinates separately.
    2) Given a set of moon positions and velocities we can calculate the state one step ahead,
       this means that any cycle must end up in the starting state
    3) The solution will be the lcm of the different cycle lengths
    """

    with open("input") as f:
        s = f.read()
    moons = parse(s)

    x = find_cycle([m.pos.x for m in moons])
    y = find_cycle([m.pos.y for m in moons])
    z = find_cycle([m.pos.z for m in moons])
    print(lcm(x, lcm(y, z)))

solve1()
solve2()
