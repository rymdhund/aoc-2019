from typing import List, Optional

def load_program() -> List[int]:
    with open("input") as f:
        return [int(n) for n in f.read().split(",")]


def step(mem: List[int], pos: int) -> Optional[int]:
    opcode = mem[pos]
    if opcode == 1:
        # Add
        mem[mem[pos+3]] = mem[mem[pos+1]] + mem[mem[pos+2]]
        return pos+4
    elif opcode == 2:
        # Mult
        mem[mem[pos+3]] = mem[mem[pos+1]] * mem[mem[pos+2]]
        return pos+4
    elif opcode == 99:
        # Exit
        return None
    assert False


def process(mem: List[int]):
    pos = 0
    while pos is not None:
        pos = step(mem, pos)


def run_day2(mem: List[int], noun: int, verb: int) -> int:
    mem[1] = noun
    mem[2] = verb
    process(mem)
    return(mem[0])


def solve1():
    mem = load_program()
    print(run_day2(mem, 12, 2))


def solve2():
    mem = load_program()
    for i in range(100):
        for j in range(100):
            if run_day2(mem[:], i, j) == 19690720:
                print(100*i + j)
                return

solve1()
solve2()
