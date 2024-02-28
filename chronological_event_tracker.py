from .event import event
from typing import *
from .memory import memory


    
class chronological_event_tracker:
    '''
    Responsiable to track the order of the last events.
    '''
    def __init__(self) -> None:
        self.__last_events: List[Tuple[event, int]] = []

    def event_happend(self, event: event):
        self.__last_events.append((event))
    
    def create_new_memory(self, intensity: int):
        '''
        Create a memory from the last events.
        '''
        return memory(events=self.__last_events, intensity=intensity)
    
        
        
