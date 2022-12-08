from pathlib import Path
from typing import Set
from time import perf_counter_ns as timestamp_nano
if __name__ == '__main__':
    start = timestamp_nano()
    pairs = Path(r'input.txt')


    def cvt(r: str) -> Set[int]:
        a, b = list(map(int, r.split('-')))
        return set(range(a, b + 1))


    # P1
    with pairs.open(mode='r') as f:
        p1 = len(list(filter(lambda r: r[0] >= r[1] or r[0] <= r[1],
                              map(lambda t: (cvt(t[0]), cvt(t[1])),
                                  map(lambda s: s.split(','), f.read().splitlines())))))

    # P2
    with pairs.open(mode='r') as f:
        p2 = len(list(filter(lambda r: not r[0].isdisjoint(r[1]),
                              map(lambda t: (cvt(t[0]), cvt(t[1])),
                                  map(lambda s: s.split(','), f.read().splitlines())))))

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')