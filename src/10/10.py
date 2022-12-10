from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import List, Iterable, Tuple, Optional
from collections import namedtuple

INST =dict(addx=2, noop=1)

@dataclass
class Inst:
    name: str
    amt: Optional[int] = None
    tick:int = 0
    
    def get_ticks_left(self):
        return INST[self.name] - self.tick
    
    def finished(self):
        return self.get_ticks_left() == 0
    
    def make_tick(self):
        self.tick+=1
        
        

class Instructions:
    R = 6
    C = 40
    
    def __init__(self, path: Path) -> None:
        with path.open() as fp:
            self.instructions = list(reversed(fp.read().splitlines()))
        self.tick = 0
        self.instruction = None
        self.X = 1
        self.board = ['' for l in range(Instructions.R)]
                
    def make_tick(self)-> int:
        self.tick+=1
        newx = self.X
        if self.instruction is None:
            n, *v=  self.instructions.pop().split(' ', maxsplit=1)
            self.instruction = Inst(n, int(v[0]) if len(v) == 1 else None)
        print(self.instruction)
        self.instruction.make_tick()
        if self.instruction.finished():
            if self.instruction.name != 'noop':
                newx = self.X + self.instruction.amt
            self.instruction = None
        return newx
    
    def get_values(self, *ticks:int):
        ticks = list(sorted(ticks))
        max_tick = ticks[-1]
        
        values = dict()
        self.board[0]+='#'
        for i in range(1, max_tick+20): # TODO HACKY AF
            r, c = i // Instructions.C, i % Instructions.C 
            newX = self.make_tick()
            self.board[r] += ('#' if self.is_lit(r,c, newX) else '.')
            
            if i in ticks:
                values[i] = self.X
            self.X = newX
        return values
          
    
    def is_lit(self, r:int, c:int, X:int)->bool:
        row = self.board[r]
        return c in (X-1,X,X+1)




if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')

    inst_set = Instructions(fp)
    values = inst_set.get_values(20,60,100,140,180,220)
    print(values)
    p1 = sum(map(lambda k: k[0]*k[1], values.items()))
    p2 = '\n'.join(inst_set.board)
    end = timestamp_nano()
    print(f"{p1=}\n")
    print(p2)
    print(f'\ntime: {(end - start) / 1000:.3f}µs')
