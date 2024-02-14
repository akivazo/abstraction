from dataclasses import dataclass
from typing import List, Mapping
from abc import abstractmethod, ABC

@dataclass
class event(ABC):
    intensity: int

    def __post_init__(self):
        if self.intensity < 1:
            raise ValueError("intensity must be graeter than 0 integer")

        
    def __add__(self, other: "event"):
        return event(self.intensity + other.intensity)

@dataclass
class eof_event:
    pass
