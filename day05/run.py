from typing import List, Optional
import sys

DEBUG = False


def debug(s):
    if DEBUG:
        print(s, file=sys.stderr)


def load_program() -> List[int]:
    with open("input") as f:
        return [int(n) for n in f.read().split(",")]


def read(mem, arg, mode) -> int:
    if mode == 0:
        return mem[arg]
    elif mode == 1:
        return arg

    assert False

def write(mem, dest, value) -> None:
    mem[dest] = value


def step(mem: List[int], pos: int) -> Optional[int]:
    assert pos < len(mem), "program counter out of range: {}".format(pos)
    assert pos >= 0, "program counter out of range: {}".format(pos)

    opcode = mem[pos] % 100
    def modes(n):
        return ((mem[pos] // (100 * (10**i))) % 10 for i in range(n))

    if opcode == 1:
        # Add
        arg1, arg2, arg3 = mem[pos+1:pos+4]
        mode1, mode2, mode3 = modes(3)
        assert mode3 == 0

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[{} + {} => {}]".format(v1, v2, arg3))
        write(mem, arg3, v1 + v2)
        return pos+4
    elif opcode == 2:
        # Mult
        arg1, arg2, arg3 = mem[pos+1:pos+4]
        mode1, mode2, mode3 = modes(3)
        assert mode3 == 0

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[{} * {} => {}]".format(v1, v2, arg3))
        write(mem, arg3, v1 * v2)
        return pos+4
    elif opcode == 3:
        # Read
        arg1 = mem[pos+1]
        mode1, = modes(1)
        assert mode1 == 0

        debug("[read => {}]".format(arg1))
        print("input:", file=sys.stderr)
        write(mem, arg1, int(input()))
        return pos+2
    elif opcode == 4:
        # Write
        arg1 = mem[pos+1]
        mode1, = modes(1)
        v1 = read(mem, arg1, mode1)
        debug("[write {}]".format(v1))
        print(v1)
        return pos+2
    elif opcode == 5:
        # jump-if-true
        arg1, arg2 = mem[pos+1:pos+3]
        mode1, mode2 = modes(2)

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[if {} goto {}]".format(v1, v2))
        if v1 != 0:
            return v2
        return pos+3
    elif opcode == 6:
        # jump-if-false
        arg1, arg2 = mem[pos+1:pos+3]
        mode1, mode2 = modes(2)

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[if-not {} goto {}]".format(v1, v2))
        if v1 == 0:
            return v2
        return pos+3
    elif opcode == 7:
        # less than
        arg1, arg2, arg3 = mem[pos+1:pos+4]
        mode1, mode2, mode3 = modes(3)
        assert mode3 == 0

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[{} < {} => {}]".format(v1, v2, arg3))
        val = 1 if v1 < v2 else 0
        write(mem, arg3, val)
        return pos+4
    elif opcode == 8:
        # equals
        arg1, arg2, arg3 = mem[pos+1:pos+4]
        mode1, mode2, mode3 = modes(3)
        assert mode3 == 0

        v1 = read(mem, arg1, mode1)
        v2 = read(mem, arg2, mode2)
        debug("[{} == {} => {}]".format(v1, v2, arg3))
        val = 1 if v1 == v2 else 0
        write(mem, arg3, val)
        return pos+4
    elif opcode == 99:
        # Exit
        return None

    assert False, "illegal opcode: {}".format(opcode)


def process(mem: List[int]):
    pos = 0
    while pos is not None:
        pos = step(mem, pos)

def test_add():
    mem = [
        1, 0, 0, 0,
        99
    ]
    process(mem)
    assert mem == [2, 0, 0, 0, 99]

def test_mult():
    mem = [
        2, 0, 0, 0,
        99
    ]
    process(mem)
    assert mem == [4, 0, 0, 0, 99]

def test_modes():
    mem = [
        1002, 4, 3, 4, 33
    ]
    process(mem)
    assert mem == [1002, 4, 3, 4, 99]

def test_read_write():
    mem = [
        3, 0,
        4, 0,
        99
    ]
    process(mem)

def run_tests():
    global DEBUG
    d = DEBUG
    DEBUG = False
    test_add()
    test_mult()
    test_modes()
    # test_read_write()
    DEBUG = d

run_tests()

def main():
    mem = load_program()
    process(mem)

main()
