from ..abstraction import abstraction
from ..event import event
from dataclasses import dataclass


class string_event(event):
    def __init__(self, string: str):
        super().__init__(intensity=sum(map(lambda c: ord(c), string)))
        self.string = string

    def __add__(self, other: "string_event"):
        return string_event(string=self.string + other.string)
    
    def __hash__(self) -> int:
        return self.string.__hash__()
    
class supply_events:
    def __init__(self, string) -> None:
        self.ind = 0
        self.string_iter = list(string).__iter__()

    def __call__(self):
        try:
            s = self.string_iter.__next__()
            return string_event(string=s)
        except StopIteration:
            return None
            

def test_empty_supplier():
    abstraction_inst = abstraction(supply_events(""))
    abstraction_inst.learn()

def test_simple_supplier():
    abstraction_inst = abstraction(supply_events("hello world"))
    abstraction_inst.learn()