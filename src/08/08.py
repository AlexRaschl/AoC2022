from functools import reduce
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import List, Iterable, Tuple


class Grid:

    def __init__(self, path_to_grid: Path):
        with path_to_grid.open('r') as f:
            self.grid = tuple(map(lambda l: tuple(map(int, l)), map(list, f.read().splitlines())))
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def visibility_matrix(self) -> List[List[bool]]:
        mat = [list([True for _ in range(self.C)]) for _ in range(self.R)]

        for r in range(self.R):
            for c in range(self.C):
                mat[r][c] = self.is_visible(r, c)
        return mat

    def scenic_scores(self) -> List[List[int]]:
        mat = [list([0 for _ in range(self.C)]) for _ in range(self.R)]
        for r in range(self.R):
            for c in range(self.C):
                mat[r][c] = self.scenic_score(r, c)
        return mat

    def is_visible(self, r: int, c: int) -> bool:
        return any([f(r, c)[0] for f in (self.above, self.below, self.left, self.right)])

    def scenic_score(self, r: int, c: int) -> int:
        return reduce(lambda a, b: a * b, [f(r, c)[1] for f in (self.above, self.below, self.left, self.right)], 1)

    def above(self, r: int, c: int) -> Tuple[bool, int]:
        v = self.grid[r][c]
        for i in reversed(range(r)):
            if self.grid[i][c] >= v:
                return False, r - i
        return True, r

    def below(self, r: int, c: int) -> Tuple[bool, int]:
        v = self.grid[r][c]
        for i in range(r + 1, self.R):
            if self.grid[i][c] >= v:
                return False, i - r
        return True, self.R - r - 1

    def left(self, r: int, c: int) -> Tuple[bool, int]:
        v = self.grid[r][c]
        for i in reversed(range(c)):
            if self.grid[r][i] >= v:
                return False, c - i
        return True, c

        # return all(map(lambda i: i < v, line[:c]))

    def right(self, r: int, c: int) -> Tuple[bool, int]:
        v = self.grid[r][c]
        for i in range(c + 1, self.C):
            if self.grid[r][i] >= v:
                return False, i - c
        return True, self.C - c - 1
        # return all(map(lambda i: i < v, line[c + 1:]))

    def __str__(self):
        return Grid.format_mat(self.grid)

    @staticmethod
    def format_mat(mat: Iterable[Iterable[int | bool]]):
        s = ''
        for r in mat:
            s += ''.join([str(int(c)) for c in r])
            s += '\n'
        return s


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')
    grid = Grid(fp)
    mat = grid.visibility_matrix()
    sc = grid.scenic_scores()
    print(grid)
    print(Grid.format_mat(mat))
    print(sc)
    p1 = sum([b for r in mat for b in r])
    p2 = max([b for r in sc for b in r])
    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
