from .event import event
from .memory import memory
from typing import *
from dataclasses import dataclass
from .event_intensity_tracker import events_intensity_tracker
import os

class unknown_memory_exception(Exception):
    def __init__(self, known_events: List[event], unknown_events: List[event]) -> None:
        self.known_events = known_events
        self.unknown_events = unknown_events
        super().__init__(",".join(self.known_events) + os.linesep + ",".join(self.unknown_events))

class event_node:
    def __init__(self, event: event) -> None:
        self.__event = event
        self.__memory: memory = None
        self.__next: Mapping[event, "event_node"] = {}

    def get_next_events(self) -> List[event]:
        return list(self.__next.keys())
    
    def get_next_event_node(self, event: event):
        return self.__next[event]
    
    def add_next(self, event: event):
        self.__next[event] = event_node(event=event)

    def get_event(self):
        return self.__event
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, __class__):
            return self.get_event() == __value.get_event()
        
    def map_to_memory(self, memory: memory):
        self.__memory = memory

    def has_memory(self):
        return self.__memory is not None
    
    def get_memory(self):
        return self.__memory

class memory_storage:
    '''
    Responsiable to remember all the memories that happend,
    and find closest known memory given a sequence of events.
    '''
    def __init__(self) -> None:
        self.__memories = set()
        self.__dummy_event_node = event_node(None)

    def add_memory(self, memory: memory):
        self.__memories.add(memory)
        current_node = self.__dummy_event_node
        internal_events = memory.get_events()
        ind = 0
        while ind < len(internal_events):
            next_event = internal_events[ind]
            known_next_events = current_node.get_next_events()
            if next_event in known_next_events:
                current_node = current_node.get_next_event_node(next_event)
            else:
                current_node.add_next(next_event)
            ind += 1
        current_node.map_to_memory(memory)
    
    def find_memories(self, events: Sequence[event]):
        ind = 0
        current_node = self.__dummy_event_node
        memories: List[Tuple[memory, float]] = []
        similarity = 1
        while ind < len(events):
            next_event = events[ind]
            next_events = current_node.get_next_events()
            next_known_event = max(
                next_events,
                key=lambda event: next_event.similarity(event),
                default=None
            )
            if next_known_event in None:
                raise unknown_memory_exception(
                    known_events=events[:ind + 1],
                    unknown_events=events[ind:])
            similarity *= next_event.similarity(next_known_event)
            current_node = current_node.get_next_event_node(next_known_event)
            if current_node.has_memory():
                memories.append((current_node.get_memory(), similarity))
        assert len(memories) > 0
        return memories
        

        
