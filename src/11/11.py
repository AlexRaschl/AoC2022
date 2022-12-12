from ast import Dict
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from time import perf_counter_ns as timestamp_nano
from typing import Callable, List, Iterable, Tuple, Optional
import re

class Monkey:
    def __init__(self, id:int, op:Callable[[int,int], int], rhd:str|int, divby:int, true_id:int, false_id:int, *items:int) -> None:
        self.id = id
        self.op = op
        self.rhd = rhd
        self.divby=divby
        self.true_id = true_id
        self.false_id = false_id
        self.items=items
        self.n_inspects = 0
        
    def inspect_next(self):
        self.items[0] = self.op(self.items[0], self.rhd if isinstance(self.rhd, int) else self.items[0])
        self.items[0]//3
        self.n_inspects+=1
    
    def throw_next(self)->Tuple[int,int]:
        itm = self.items.pop(0)
        m_id = self.true_id if itm % self.divby==0 else self.false_id
        return m_id, itm

    def catch(self,item:int):
        self.items.append(item)
    
    def has_item(self)->bool:
        return len(self.items) > 0
    
    @staticmethod
    def create_from(mObj: re.Match)->'Monkey':
        gd = mObj.groupdict()
        # TODO init stuff
    
class KeepAway:
    # https://regex101.com/r/colAii/1
    REGEX = re.compile('(?:Monkey\s(?P<m_id>\d+):\n\s+Starting\sitems:\s(?P<items>(?:\d+[, \n]+)+))\s{2}Operation:\snew = old (?P<op>[+\-*\/]) (?P<rhd_oprnd>\d+|old)\n\s{2}Test: divisible by (?P<divby>\d+)\n\s{4}If true: throw to monkey (?P<true_id>\d+)\n\s{4}If false: throw to monkey (?P<false_id>\d+)\s*')
    def __init__(self, path: Path) -> None:
        with path.open('r') as fp:
            self.constellation = fp.read()
        self.monkeys: Dict[int, Monkey] = self.init_monkeys(self.constellation)
        
    
    @staticmethod
    def init_monkeys(starting_constellation:str)->Dict[int,Monkey]:
        monkeys = {}
        for match in re.finditer(KeepAway.REGEX, starting_constellation):
            m = Monkey.create_from(match)
            monkeys[m.id] = m
        return monkeys
    

    def play(self, rounds: int)->int:
        for i in range(rounds):
            self.play_round()
        return reduce(lambda a,b: a*b, reversed(sorted([m.inspects for m in self.monkeys.values()]))[:2],1)
   
        
        
    def play_round(self):
        for i, m in self.monkeys.items():
            while m.has_item():
                m.inspect_next()
                m_id, itm = m.throw_next()
                self.monkeys[m_id].catch(itm)
            
    


if __name__ == '__main__':
    start = timestamp_nano()
    fp = Path(r'input.txt')
    ka = KeepAway(fp)
    p1 = ka.play(rounds=20)
    

    end = timestamp_nano()
    # print(f"{p1=}")
    # print(f"{p2=}")
    print(f'time: {(end - start) / 1000:.3f}µs')
    
    