from pathlib import Path
from functools import reduce

if __name__ == '__main__':
    rucksacks = Path(r'input.txt')

    # P1
    with rucksacks.open(mode='r') as f:
        print(list(map(lambda s: tuple(set(s[:len(s) // 2]).intersection(s[len(s) // 2:]))[0], f.read().splitlines())))
        f.seek(0)
        print(list(map(lambda c: ord(c) - ord('a' if c.islower() else 'A') + 1,
                       map(lambda s: tuple(set(s[:len(s) // 2]).intersection(s[len(s) // 2:]))[0],
                           f.read().splitlines()))))
        f.seek(0)
        print(sum(map(lambda c: ord(c) - (ord('a') if c.islower() else (ord('A') - 26)) + 1,
                      map(lambda s: set(s[:len(s) // 2]).intersection(s[len(s) // 2:]).pop(),
                          f.read().splitlines()))))

    # P2
    with rucksacks.open(mode='r') as f:
        rs = list(map(set, f.read().splitlines()))
        triplets = [rs[x:x + 3] for x in range(0, len(rs), 3)]
        print(sum(map(lambda c: ord(c) - (ord('a') if c.islower() else (ord('A') - 26)) + 1,
                      map(lambda tr: reduce(lambda t1, t2: t1 & t2, tr).pop(), triplets))))
