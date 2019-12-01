with open("input") as f:
    inp = [int(n) for n in f.read().split("\n") if n]

sol1 = sum(m // 3 - 2 for m in inp)
print(sol1)

def with_gas_gas(mass):
    g = mass // 3 - 2
    if g <= 0:
        return 0
    return g + with_gas_gas(g)

sol2 = sum(with_gas_gas(m) for m in inp)
print(sol2)
