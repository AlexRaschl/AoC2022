from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import List, Iterable, Tuple, Optional


@dataclass
class Node:
    r: int
    c: int
    name: str
    sign: str
    next: 'Node' = None

    def move(self, direction: str) -> Tuple[int, int]:
        if direction == 'U':
            self.r += 1
        elif direction == 'D':
            self.r -= 1
        elif direction == 'R':
            self.c += 1
        elif direction == 'L':
            self.c -= 1
        return self.move_too()

    def move_too(self) -> Optional[Tuple[int, int]]:
        if self.next is None:
            return self.coords
        if self.next.needs_follow(self):
            next_move = self.next.determine_move(self)
            if next_move is not None:
                self.next.coords = next_move
                return self.next.move_too()
        else:
            return None

    def determine_move(self, parent:'Node')->Tuple[int,int]:
        dist = self.dist(parent)
        if dist <= 1:
            # No move needed
            return None
        elif dist == 2:
            if self.r == parent.r:
                 # move right or left
                return (self.r, self.c + sign(parent.c - self.c))
            elif self.c == parent.c:
                # move up ord down
                return (self.r + sign(parent.r - self.r), self.c)
            else:
                return None # Diagonal do nothing
        elif dist >= 3:# and not (self.r == parent.r or self.c == parent.c):
            # Diagonal move
            return (self.r + sign(parent.r - self.r), self.c+ sign(parent.c - self.c))
        else:
            return None



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



def sign(i: int)-> int:
    return -1 if i < 0 else 1


class HeadTail:

    def __init__(self, input: Path, n: int = 2):
        assert n >= 2
        with input.open() as f:
            self.moves = f.read().splitlines()

        self.h = Node(0, 0, 'head', 'H')
        self.nodes = [self.h]
        p = self.h
        for i in range(n - 1):
            n = Node(0, 0, 'node_' + str(i), str(i))
            self.nodes.append(n)
            p.next = n
            p = n

        self.t = p
        self.tail_moves = set([self.t.coords])

    def play_game(self):
        for move in self.moves:
            t, amt = move.split(' ', 1)
            print(f"MOVE: {move}")
            self.execute(t, int(amt))

    def execute(self, move: str, amt: int):
        for i in range(amt):
            moved_to = self.h.move(move)
            # print(self)
            # print('\n\n')
            if moved_to is not None:
                self.tail_moves.add(moved_to)

    def __str__(self):
        coords = [(0, 0), *[n.coords for n in self.nodes]]
        rs, cs = list(zip(*coords))
        border = 6
        rmin, rmax = sorted(rs)[::len(rs) - 1]
        cmin, cmax = sorted(cs)[::len(cs) - 1]
        width, height = cmax - cmin + border, rmax - rmin + border
        rs_cvt = [r + rmin+ border//2 for r in rs]
        cs_cvt = [c + cmin+ border//2 for c in cs]
        shft_coords = set(list(zip(rs_cvt, cs_cvt)))
        cmap = dict(zip(list(zip(rs_cvt, cs_cvt)), list('SH' + ''.join(map(str, range(1, len(self.nodes)))))))

        field = []
        for i in range(height):
            field.append('')
            for j in range(width):
                if (i, j) in shft_coords:
                    field[i] += cmap[(i,j)]
                else:
                    field[i] += '.'
        return '\n'.join(field)


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')

    game = HeadTail(fp)
    game.play_game()
    p1 = len(game.tail_moves)

    game = HeadTail(fp, 10)
    game.play_game()
    print(game.tail_moves)
    p2 = len(game.tail_moves)

    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
