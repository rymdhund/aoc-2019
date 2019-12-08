from typing import List, Optional
import sys
import itertools

DEBUG = False


def debug(s):
    if DEBUG:
        print(s, file=sys.stderr)


def load_program() -> List[int]:
    with open("input") as f:
        return [int(n) for n in f.read().split(",")]


class Program:
    def __init__(self, mem, inp):
        self.mem = mem
        self.inp = inp
        self.out = []
        self.pos = 0

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
            return self.mem[arg]
        elif mode == 1:
            return arg

        assert False

    def write(self, dest, value) -> None:
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
            assert mode3 == 0

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            debug("[{} + {} => {}]".format(v1, v2, arg3))
            self.write(arg3, v1 + v2)
            self.pos += 4
        elif opcode == 2:
            # Mult
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)
            assert mode3 == 0

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            debug("[{} * {} => {}]".format(v1, v2, arg3))
            self.write(arg3, v1 * v2)
            self.pos += 4
        elif opcode == 3:
            # Read
            arg1 = self.mem[self.pos+1]
            mode1, = modes(1)
            assert mode1 == 0

            debug("[read => {}]".format(arg1))
            self.write(arg1, self.inp.pop(0))
            self.pos += 2
        elif opcode == 4:
            # Write
            arg1 = self.mem[self.pos+1]
            mode1, = modes(1)
            v1 = self.read(arg1, mode1)
            debug("[write {}]".format(v1))
            self.out.append(v1)
            self.pos += 2
        elif opcode == 5:
            # jump-if-true
            arg1, arg2 = self.mem[self.pos+1:self.pos+3]
            mode1, mode2 = modes(2)

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            debug("[if {} goto {}]".format(v1, v2))
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
            debug("[if-not {} goto {}]".format(v1, v2))
            if v1 == 0:
                self.pos = v2
            else:
                self.pos += 3
        elif opcode == 7:
            # less than
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)
            assert mode3 == 0

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            debug("[{} < {} => {}]".format(v1, v2, arg3))
            val = 1 if v1 < v2 else 0
            self.write(mem, arg3, val)
            self.pos += 4
        elif opcode == 8:
            # equals
            arg1, arg2, arg3 = self.mem[self.pos+1:self.pos+4]
            mode1, mode2, mode3 = modes(3)
            assert mode3 == 0

            v1 = self.read(arg1, mode1)
            v2 = self.read(arg2, mode2)
            debug("[{} == {} => {}]".format(v1, v2, arg3))
            val = 1 if v1 == v2 else 0
            self.write(arg3, val)
            self.pos += 4
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

def run_tests():
    global DEBUG
    d = DEBUG
    DEBUG = False
    test_add()
    test_mult()
    test_modes()
    test_read_write()
    test_thruster_1()
    test_thruster_2()
    DEBUG = d

run_tests()


def solve1():
    mem = load_program()
    mx = 0
    for p in itertools.permutations([0, 1, 2, 3, 4]):
        v = thrust(mem, p)
        if v > mx:
            mx = v
    print(mx)


def solve2():
    mem = load_program()
    mx = 0
    for p in itertools.permutations([5, 6, 7, 8, 9]):
        v = thrust2(mem, p)
        if v > mx:
            mx = v
    print(mx)


solve1()
solve2()
