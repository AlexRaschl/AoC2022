from pathlib import Path
import itertools as it
from time import perf_counter_ns as timestamp_nano

calories = Path(r'input.txt')

if __name__ == '__main__':
    start = timestamp_nano()
    # P1
    with calories.open(mode='r') as f:
        p1 = max(map(lambda l: sum(map(int, l)),
                     [list(g) for k, g in it.groupby(f.read().splitlines(), key=lambda x: x == '') if not k]))

    # P2
    with calories.open(mode='r') as f:
        p2 = sum(sorted(map(lambda l: sum(map(int, l)),
                            [list(g) for k, g in it.groupby(f.read().splitlines(), key=lambda x: x == '') if not k]),
                        reverse=True)[:3])
    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
