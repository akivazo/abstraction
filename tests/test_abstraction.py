from ..abstraction import abstraction
from ..event import event, event_supplier_impl, end_of_big_event
from typing import List
import sys


class char_event(event):
    def __init__(self, c: str):
        super().__init__(intensity=1)
        self.char = c

    def __add__(self, other: "char_event"):
        return char_event(c=self.char + other.char)
    
    def __hash__(self) -> int:
        return self.char.__hash__()
    
    def __repr__(self) -> str:
        return self.char
    
class char_event_supplier(event_supplier_impl):
    class event_need_to_Be_char_exception(Exception):
        def __init__(self, s: str) -> None:
            super().__init__(f"event should be only one character, got '{s}'")

    def __init__(self, string: str) -> None:
        super().__init__()
        for w in string.split(" "):
            for c in w:
                self.add_char(c=c)
            self.add_event(end_of_big_event())


    def add_char(self, c: str):
        if len(c) > 1:
            raise char_event_supplier.event_need_to_Be_char_exception(c)
        return super().add_event(char_event(c))

import pytest

@pytest.mark.parametrize(["input", "result"], 
                         [
                            ("", []),
                            ("helo", ['h', 'e', 'l', 'o']),
                            ("helo my ward", ["helo", "my", "ward"]),
                            ("hello world", ["hello", "world"]),
                        ])

def test_char_supplier(input, result):
    abstraction_inst = abstraction(char_event_supplier(input))
    abstraction_inst.learn()
    events: List[char_event] = abstraction_inst.show_abstraction()
    assert list(map(lambda event: event.char, events)) == result
