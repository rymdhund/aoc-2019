from typing import List, Optional
import sys
import itertools


def load_program() -> List[int]:
    with open("input") as f:
        return [int(n) for n in f.read().split(",")]


class Program:
    def __init__(self, mem, inp, *, debug=False):
        self.mem = mem
        self.inp = inp
        self.out = []
        self.pos = 0
        self.rb = 0
        self.debug = debug

    def log(self, s):
        if self.debug:
            print(s, file=sys.stderr)


    def run(self) -> None:
        while self.pos is not None:
            self.step()

    def run_out(self) -> Optional[int]:
        while self.pos is not None:
            if self.out:
                return self.out.pop(0)
            self.step()
        return None

    def read(self, arg, mode) -> int:
        if mode == 0:
            if arg >= len(self.mem):
                return 0  # uninitialized memory
            return self.mem[arg]
        elif mode == 1:
            return arg
        elif mode == 2:
            addr = self.rb + arg
            if addr >= len(self.mem):
                return 0  # uninitialized memory
            return self.mem[addr]

        else:
            assert False

    def write(self, dest, mode, value) -> None:
        assert mode == 0 or mode == 2
        if mode == 2:
            dest += self.rb

        if dest >= len(self.mem):
            self.mem.extend((0 for _ in range(dest - len(self.mem) + 100)))
        self.mem[dest] = value

    def step(self):
        assert self.pos < len(self.mem), "program counter out of range: {}".format(self.pos)
        assert self.pos >= 0, "program counter out of range: {}".format(self.pos)

        opcode = self.mem[self.pos] % 100
        def modes(n):
            return ((self.mem[self.pos] // (100 * (10**i))) % 10 for i in range(n))

        if opcode == 1:
            # Add
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[{} + {} => {}]".format(v1, v2, arg3))
            self.write(arg3, mode3, v1 + v2)
            self.pos += 4
        elif opcode == 2:
            # Mult
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[{} * {} => {}]".format(v1, v2, arg3))
            self.write(arg3, mode3, v1 * v2)
            self.pos += 4
        elif opcode == 3:
            # Read
            arg1 = self.mem[self.pos+1]
            mode1, = modes(1)
            assert mode1 == 0 or mode1 == 2

            self.log("[read => {}]".format(arg1))
            self.write(arg1, mode1, self.inp.pop(0))
            self.pos += 2
        elif opcode == 4:
            # Write
            arg1 = self.mem[self.pos+1]
            mode1, = modes(1)
            v1 = self.read(arg1, mode1)
            self.log("[write {}]".format(v1))
            self.out.append(v1)
            self.pos += 2
        elif opcode == 5:
            # jump-if-true
            arg1, arg2 = self.mem[self.pos+1:self.pos+3]
            mode1, mode2 = modes(2)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[if {} goto {}]".format(v1, v2))
            if v1 != 0:
                self.pos = v2
            else:
                self.pos += 3
        elif opcode == 6:
            # jump-if-false
            arg1, arg2 = self.mem[self.pos+1:self.pos+3]
            mode1, mode2 = modes(2)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[if-not {} goto {}]".format(v1, v2))
            if v1 == 0:
                self.pos = v2
            else:
                self.pos += 3
        elif opcode == 7:
            # less than
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[{} < {} => {}]".format(v1, v2, arg3))
            val = 1 if v1 < v2 else 0
            self.write(arg3, mode3, val)
            self.pos += 4
        elif opcode == 8:
            # equals
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            self.log("[{} == {} => {}]".format(v1, v2, arg3))
            val = 1 if v1 == v2 else 0
            self.write(arg3, mode3, val)
            self.pos += 4
        elif opcode == 9:
            # adjust rb
            arg1 = self.mem[self.pos+1]
            mode1, = modes(1)
            v1 = self.read(arg1, mode1)
            self.log("[rb += {}]".format(v1))
            self.rb += v1
            self.pos += 2
        elif opcode == 99:
            # Exit
            self.pos = None
        else:
            assert False, "illegal opcode: {}".format(opcode)


def test_add():
    mem = [
        1, 0, 0, 0,
        99
    ]
    p = Program(mem, [])
    p.run()
    assert p.mem == [2, 0, 0, 0, 99]

def test_mult():
    mem = [
        2, 0, 0, 0,
        99
    ]
    p = Program(mem, [])
    p.run()
    assert p.mem == [4, 0, 0, 0, 99]

def test_modes():
    mem = [
        1002, 4, 3, 4, 33
    ]
    p = Program(mem, [])
    p.run()
    assert p.mem == [1002, 4, 3, 4, 99]

def test_read_write():
    mem = [
        3, 0,
        4, 0,
        99
    ]
    p = Program(mem, [1])
    p.run()
    assert p.out == [1]

def thrust(mem, seq):
    inp = 0
    for s in seq:
        p = Program(mem[:], [s, inp])
        p.run()
        inp = p.out[0]
    return inp

def thrust2(mem, seq):
    inp = 0
    programs = [Program(mem[:], [s]) for s in seq]
    i = 0
    last = 0
    while True:
        programs[i % 5].inp.append(inp)
        out = programs[i % 5].run_out()
        if out is None:
            return inp
        inp = out
        i += 1

def test_thruster_1():
    mem = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    t = thrust(mem, [4,3,2,1,0])
    assert t == 43210

def test_thruster_2():
    mem = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    t = thrust2(mem, [9, 8, 7, 6, 5])
    assert t == 139629729

def test_quine():
    mem = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    p = Program(mem, [])
    p.run()
    assert p.out == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

def run_tests():
    test_add()
    test_mult()
    test_modes()
    test_read_write()
    test_thruster_1()
    test_thruster_2()
    test_quine()

def move(pos, dir, turn):
    if turn == 0:
        dir = (dir + 1) % 4
    elif turn == 1:
        dir = (dir - 1) % 4
    else:
        assert False

    x, y = pos
    dx, dy = 0, 0
    if dir == 0:
        dy = -1
    elif dir == 1:
        dx = -1
    elif dir == 2:
        dy = 1
    elif dir == 3:
        dx = 1
    else:
        assert False

    return (x+dx, y+dy), dir

run_tests()


def display_coord_dict(coords):
    def value_to_char(v):
        return "█" if v == 0 else " "

    default_v = 0
    minx, miny = next(coords.keys().__iter__())
    maxx, maxy = minx, miny

    for x, y in coords:
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y

    for row in range(miny, maxy+1):
        s = ""
        for col in range(minx, maxx+1):
            v = coords.get((col,row), default_v)
            s += value_to_char(v)
        print(s)


def robot(mem, hull):
    p = Program(mem, [])
    pos = (0, 0)
    dir = 0 # up
    while True:
        color = hull.get(pos, 0)
        p.inp.append(color)

        color = p.run_out()
        if color == None:
            break
        hull[pos] = color
        turn = p.run_out()
        pos, dir = move(pos, dir, turn)
    return hull


def solve1():
    hull = robot(load_program(), {})
    print(len(hull))


def solve2():
    hull = robot(load_program(), {(0,0): 1})
    display_coord_dict(hull)


solve1()
solve2()
