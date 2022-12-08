import re
from pathlib import Path
from typing import List, Literal
from collections import defaultdict
from time import perf_counter_ns as timestamp_nano


class Board:
    BOARD_REGEX = re.compile(r"\[([A-Z])] ?|    ")
    MOVE_REGEX = re.compile(r"move (?P<amount>\d+) from (?P<from>\d+) to (?P<to>\d+)")

    def __init__(self, playground: str, movertype: Literal['9000', '9001'] = '9001'):
        lines = playground.splitlines()
        self.stacks = defaultdict(list)
        self.fill_stacks(lines[:-1])
        self.move_at_once = movertype == '9001'

    def play(self, moves: List[str], debug: bool = False) -> str:
        for m in moves:
            self.perform_move(m, debug)
            if debug:
                print(self)
        return ''.join([s[-1] for s in self.stacks.values()])

    def perform_move(self, move: str, debug: bool):
        amt, from_, to = tuple(map(int, re.fullmatch(Board.MOVE_REGEX, move).groupdict().values()))
        if debug:
            print(f'moving {amt} from {from_} to {to}')
        # P1
        if not self.move_at_once:
            for _ in range(amt):
                crate = self.stacks[from_].pop()
                if debug:
                    print(f'\tmoving [{crate}] from {from_} to {to}')
                self.stacks[to].append(crate)
        # P2
        else:
            self.stacks[to].extend(self.stacks[from_][-amt:])
            if debug:
                print(f'\tmoving [{"] [".join(self.stacks[from_][-amt:])}] from {from_} to {to}')
            self.stacks[from_] = self.stacks[from_][:-amt]

    def __str__(self):
        s = ''
        for k, stack in self.stacks.items():
            s += f'{k}: {" ".join(["[" + n + "]" for n in stack])}\n'
        return s

    def fill_stacks(self, lines):
        for line in lines[::-1]:
            [self.stacks[i + 1].append(match) for i, match in enumerate(re.findall(Board.BOARD_REGEX, line)) if match]


if __name__ == '__main__':
    start = timestamp_nano()

    fp = Path(r'input.txt')

    with fp.open() as f:
        playground, moves = f.read().split('\n\n', maxsplit=1)

    moves = moves.split('\n')
    board = Board(playground, movertype='9000')
    p1 = board.play(moves, debug=True)
    board = Board(playground, movertype='9001')
    p2 = board.play(moves, debug=True)
    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
