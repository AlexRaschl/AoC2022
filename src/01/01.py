from pathlib import Path
import itertools as it

calories = Path(r'input.txt')

# P1
with calories.open(mode='r') as f:
    print(max(map(lambda l: sum(map(int, l)),
                  [list(g) for k, g in it.groupby(f.read().splitlines(), key=lambda x: x == '') if not k])))

# P2
with calories.open(mode='r') as f:
    print(sum(sorted(map(lambda l: sum(map(int, l)),
                         [list(g) for k, g in it.groupby(f.read().splitlines(), key=lambda x: x == '') if not k]),
                     reverse=True)[:3]))


