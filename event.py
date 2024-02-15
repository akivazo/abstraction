from dataclasses import dataclass
from typing import Any, List, Mapping
from abc import abstractmethod, ABC


@dataclass
class event(ABC):
    intensity: int

    def __post_init__(self):
        if self.intensity < 1:
            raise ValueError("intensity must be graeter than 0")

        
    def __add__(self, other: "event"):
        return event(self.intensity + other.intensity)

class event_supplier(ABC):
    @abstractmethod
    def __call__(self) -> event:
        pass

class event_supplier_impl(event_supplier):
    def __init__(self) -> None:
        self.__events_queue = []

    def add_event(self, event: event):
        self.__events_queue.append(event)

    def __call__(self) -> Any:
        try:
            event = self.__events_queue.pop()
            return event
        except IndexError:
            return None
@dataclass
class eof_event:
    pass
