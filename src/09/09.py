from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import List, Iterable, Tuple


@dataclass
class Node:
    r: int
    c: int
    name: str
    sign: str
    prev: 'Node' = None

    def move(self, direction: str) -> Tuple[int, int]:
        prev = self.coords
        if direction == 'U':
            self.r += 1
        elif direction == 'D':
            self.r -= 1
        elif direction == 'R':
            self.c += 1
        elif direction == 'L':
            self.c -= 1
        return self.move_to(prev)

    def move_to(self, prev: Tuple[int, int]) -> Tuple[int, int]:
        if self.prev is None:
            return self.coords
        if self.prev.needs_follow(self):
            preprev = self.prev.coords
            self.prev.coords = prev
            return self.prev.move_to(preprev)

    def needs_follow(self, node: 'Node') -> bool:
        dist = self.dist(node)
        return dist > 2 or dist == 2 and (self.r == node.r or self.c == node.c)

    @property
    def coords(self) -> Tuple[int, int]:
        return self.r, self.c

    @coords.setter
    def coords(self, coords):
        self.r, self.c = coords

    def dist(self, node: 'Node') -> int:
        return abs(self.r - node.r) + abs(self.c - node.c)


class HeadTail:

    def __init__(self, input: Path, nodes: int = 2):
        with input.open() as f:
            self.moves = f.read().splitlines()

        self.h = Node(0, 0, 'head', 'H')
        prev = self.h
        for i in range(nodes - 1):
            n = Node(0, 0, 'node_' + str(i), str(i))
            prev.prev = n
            prev = n

        self.t = prev
        self.tail_moves = set([self.t.coords])

    def play_game(self):
        for move in self.moves:
            t, amt = move.split(' ', 1)
            self.execute(t, int(amt))

    def execute(self, move: str, amt: int):
        for i in range(amt):
            self.tail_moves.add(self.h.move(move))

    # def follow(self):
    #     if self.t.needs_follow(self.h):
    #         self.t.coords = self.prev
    #         self.tail_moves.add(self.t.coords)


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')

    game = HeadTail(fp, 2)
    game.play_game()
    p1 = len(game.tail_moves)

    game = HeadTail(fp, 9)
    game.play_game()
    p2 = len(game.tail_moves)

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
