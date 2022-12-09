from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import List, Dict, Iterable, Tuple
import re
from pprint import pformat


@dataclass
class BaseFile:
    name: str

    def get_size(self) -> int:
        raise NotImplemented()


@dataclass
class Dir(BaseFile):
    parent: 'Dir'
    contents: List[BaseFile] = field(default_factory=list)

    def get_size(self) -> int:
        return sum(map(lambda c: c.get_size(), self.contents))

    def cd(self, name):
        if name == '/':
            return self.root
        if name == '..':
            return self.parent
        else:
            return next(filter(lambda d: d.name == name, filter(lambda c: isinstance(c, Dir), self.contents)))

    @property
    def root(self):
        x = self
        while x.name != '/':
            x = x.parent
        return x

    def dirs(self) -> Iterable['Dir']:
        # noinspection PyTypeChecker
        return filter(lambda c: isinstance(c, Dir), self.contents)

    @property
    def abspath(self):
        parents = [self.name]
        x = self
        while x.parent.name != '/':
            parents.append(x.parent.name)
            x = x.parent
        return '/' + '/'.join(parents[::-1])
    # def __repr__(self):
    #     return f'DIR {self.name}\n' + pformat(self.contents, indent=3)


@dataclass
class File(BaseFile):
    size: int

    def get_size(self) -> int:
        return self.size

    def __repr__(self):
        return f'{self.size} {self.name}'


class CLI:
    P_CMD = '(?P<cmd>cd|ls)\s*(?P<arg>\S*)?'
    P_RES = '(?:dir\s(?P<dir>\S*))|(?:(?P<fsize>\d*)\s(?P<fname>\S*))\n'

    def __init__(self, debug: bool = False):
        # noinspection PyTypeChecker
        self.root = Dir(name='/', parent=None)
        self.root.parent = self.root
        self.wd = self.root
        self._debug = debug

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug: bool):
        self._debug = debug

    def parse_all_commands(self, commands: Iterable[str] | str) -> None:
        if isinstance(commands, str):
            commands = commands.split('$ ')[1:]

        for cmd in commands:
            self.parse(cmd)
            if self.debug:
                print(self.root)

    def parse(self, cmd: str) -> None:
        c, res = cmd.split('\n', maxsplit=1)
        cmatch = re.match(CLI.P_CMD, c)
        c = cmatch.groupdict().get('cmd')
        arg = cmatch.groupdict().get('arg')
        if self.debug:
            print(f'CMD: {c}, ARG: {arg}, WD: {self.wd.name}, WDC: {self.wd.contents}')
        if c == 'cd':
            self.wd = self.wd.cd(arg)
        elif c == 'ls':
            assert arg == ''
            for match in re.finditer(CLI.P_RES, res):
                self._populate(match.groupdict())
        else:
            raise ValueError(f'Invalid command: {c}')

    def _populate(self, result_match: Dict[str, str]) -> None:
        if d := result_match.get('dir'):
            dir_ = Dir(d, parent=self.wd)
            self.wd.contents.append(dir_)
        else:
            fname = result_match.get('fname')
            fsize = int(result_match.get('fsize'))
            file = File(fname, fsize)
            self.wd.contents.append(file)

    def __str__(self):
        return str(self.root)

    @staticmethod
    def get_flatmap_dir_sizes(root: Dir) -> List[Tuple[str, int]]:
        size_dict = {root.abspath: root.get_size()}
        for p, d in zip(map(lambda k: k.abspath, root.dirs()), root.dirs()):
            sub_dirs = CLI.get_flatmap_dir_sizes(d)
            size_dict.update(sub_dirs)

        return list(sorted(size_dict.items(), key=lambda t: -t[1]))


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')
    with fp.open() as f:
        commands = f.read()

    cli = CLI(debug=False)
    cli.parse_all_commands(commands)
    sizes = CLI.get_flatmap_dir_sizes(cli.root)
    p1 = sum(map(lambda s: s[1], filter(lambda s: s[1] <= 100_000, sizes)))
    fs_size = cli.root.get_size()
    total_size = 70_000_000
    req_size = 30_000_000
    diff = abs(total_size - fs_size - req_size)
    p2 = list(filter(lambda s: s[1] > diff, sizes))[-1]
    end = timestamp_nano()
    print(f"{p1=}")
    print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
