from pathlib import Path
from time import perf_counter_ns as timestamp_nano

def all_different(chars: str):
    return len(set(chars)) == len(chars)

def find_all_distinct(signal: str, marker_length:int) -> int:
    assert len(signal) >= marker_length
    stack = signal[:marker_length]
    for i,s in enumerate(signal[marker_length:], start=marker_length):
        if all_different(stack):
            return i
        stack = stack[1:] + s
    return -1


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')

    with fp.open() as f:
        signal = f.read()
    p1 = find_all_distinct(signal, marker_length=4)
    p2 = find_all_distinct(signal, marker_length=14)

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
