from dataclasses import dataclass
from typing import Any, List, Mapping
from abc import abstractmethod, ABC


class event(ABC):
    def __init__(self, intensity):
        self.intensity = intensity
        if self.intensity < 1:
            raise ValueError("intensity must be graeter than 0")
        
    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, event):
            return self.__hash__() == __value.__hash__()
        return False
        
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
        if len(self.__events_queue) > 0:
            event = self.__events_queue.pop(0)
            return event
        return eof_event()

class eof_event(event):
    _instance = None
    
    def __init__(self):
        self.intensity = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(eof_event, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def __hash__(self) -> int:
        return -1
    
