from pathlib import Path
from functools import reduce
from time import perf_counter_ns as timestamp_nano
if __name__ == '__main__':
    start = timestamp_nano()
    rucksacks = Path(r'input.txt')
    # P1
    with rucksacks.open(mode='r') as f:
        p1 = sum(map(lambda c: ord(c) - (ord('a') if c.islower() else (ord('A') - 26)) + 1,
                      map(lambda s: set(s[:len(s) // 2]).intersection(s[len(s) // 2:]).pop(),
                          f.read().splitlines())))

    # P2
    with rucksacks.open(mode='r') as f:
        rs = list(map(set, f.read().splitlines()))
        triplets = [rs[x:x + 3] for x in range(0, len(rs), 3)]
        p2 = sum(map(lambda c: ord(c) - (ord('a') if c.islower() else (ord('A') - 26)) + 1,
                      map(lambda tr: reduce(lambda t1, t2: t1 & t2, tr).pop(), triplets)))

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')