from .event import event
from typing import *

class memory:
    '''
    an event that was construct from several 'small' events
    '''
    def __init__(self, events: Sequence[event], intensity: int) -> None:
        if len(events) < 2:
            raise Exception("a memory should be made from at least one events")
        self.__events = tuple(events)
        self.__intensity = intensity

    def get_events(self):
        return self.__events
    
    def __hash__(self) -> int:
        return self.__events.__hash__()