from pathlib import Path
import itertools as it
from enum import Enum
from typing import Literal, Tuple, Iterable

from time import perf_counter_ns as timestamp_nano
def get_points(ab: Iterable[str]) -> int:
    a, b = ab
    a = shape_matches[a]
    a_sc, b_sc = shape_scores[a], shape_scores[b]
    diff = b_sc - a_sc
    return ((diff + 1) % 3) * 3 + b_sc


def get_pointsv2(ab: Iterable[str]) -> int:
    a, b = ab
    a = shape_matches[a]
    a_sc, b_sc = shape_scores[a], shape_scores[b]
    shift = (b_sc - 2)

    return ((shift + 1) % 3) * 3 + (a_sc + shift - 1) % 3 + 1


if __name__ == '__main__':
    start = timestamp_nano()
    strategy = Path(r'input.txt')

    shape_scores = dict(X=1, Y=2, Z=3)
    shape_matches = dict(A='X', B='Y', C='Z')

    # P1
    with strategy.open(mode='r') as f:
        p1 = sum(map(get_points, map(str.split, f.read().splitlines())))

    # P2
    with strategy.open(mode='r') as f:
        p2 = sum(map(get_pointsv2, map(str.split, f.read().splitlines())))

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')