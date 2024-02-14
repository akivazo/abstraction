from ..abstraction import abstraction
from ..event import event

class supply_events:
    def __init__(self, string) -> None:
        self.ind = 0
        self.string_iter = list(string).__iter__()

    def __call__(self):
        try:
            return self.string_iter.__next__()
        except StopIteration:
            return None
            

def test_empty_supplier():
    abstraction_inst = abstraction(supply_events(""))
    abstraction_inst.learn()

def test_simple_supplier():
    abstraction_inst = abstraction(supply_events("hello world"))
    abstraction_inst.learn()