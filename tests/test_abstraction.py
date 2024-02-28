from ..abstraction import abstraction, unknown_events_exception, missign_next_event_exception
from ..event import event, event_supplier_impl, seperator
from typing import List
import pytest


class string_event(event):
    def __init__(self, s: str):
        super().__init__()
        self.string = s

    def __add__(self, other: "string_event"):
        return string_event(s=self.string + other.string)
    
    def __hash__(self) -> int:
        return self.string.__hash__()
    
    def __repr__(self) -> str:
        return self.string
    
class space_seperator(seperator):
    def __hash__(self) -> int:
        return ord(" ")

class dot_seperator(seperator):
    def __hash__(self) -> int:
        return ord(".")

class char_event_supplier(event_supplier_impl):

    def __init__(self, string: str) -> None:
        self.space_seperator = dot_seperator()
        self.dot_seperator = dot_seperator()

        super().__init__([self.space_seperator, self.dot_seperator])
        if len(string) == 0:
            return
        for sentence in string.split("."):
            for word in sentence.split(" "):
                for char in word:
                    self.add_char(c=char)
                self.add_seperator(self.space_seperator)
            self.add_seperator(self.dot_seperator)

    def add_seperator(self, seperator: seperator):
        self.add_event(event=seperator, intensity=0)

    def add_char(self, c: str):
        assert len(c) == 1
        intensity = 1 if c.islower() else 2
        return self.add_event(string_event(c), intensity=intensity)
    
def create_events(chars):
    return list(map(string_event, list(chars)))

@pytest.mark.parametrize(["input", "question"], [
    ("", 'h'),
    ("abcdefg", "z")
])
def test_empty_supplier(input, question):
    abstraction_inst = abstraction(char_event_supplier(input))
    abstraction_inst.learn()
    try:
        abstraction_inst.responde(create_events(question))
    except unknown_events_exception as e:
        assert e.unknown_events == [string_event(question)]
    assert False

@pytest.mark.parametrize(["input", "question"], [
    ("abcdefg", 'g'),
    ("abc gyt", "t"),
    ("abc", "bc")
])
def test_no_next_event(input, question):
    abstraction_inst = abstraction(char_event_supplier(input))
    abstraction_inst.learn()
    with pytest.raises(missign_next_event_exception, match=question):
        abstraction_inst.responde(create_events(question))
    

@pytest.mark.parametrize(["input", "question", "result"], 
                         [
                            ("helo", 'hel', 'o'),
                            ("helo my ward", "my", "w")
                        ])
def test_char_supplier(input, question, result):
    abstraction_inst = abstraction(char_event_supplier(input))
    abstraction_inst.learn()
    events: List[string_event] = abstraction_inst.responde(create_events(question))
    assert list(map(lambda event: event.string, events)) == result

@pytest.mark.parametrize(["study", "question", "ecpected_answer"], 
                         [
                             ("hello world", "hello", "world"),
                             ("hello world", "helo", "world"),
                         ])
def test_get_events_follow_up(study, question, ecpected_answer):
    abstraction_inst = abstraction(char_event_supplier(study))
    abstraction_inst.learn()
    answer: string_event = abstraction_inst.responde(list(map(lambda c: string_event(c), question)))
    assert answer.string == ecpected_answer

