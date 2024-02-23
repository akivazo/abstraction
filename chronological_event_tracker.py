from .event import event
from dataclasses import dataclass
from typing import Set, Mapping, List



class chronological_event_node:
    def __init__(self, event: event) -> None:
        self.__event = event
        self.__next: Set[chronological_event_node] = set()

    def add_next(self, node: "chronological_event_node"):
        self.__next.add(node)

    def get_next_nodes(self):
        return self.__next
    
    def get_event(self):
        return self.__event
    
class chronological_event_tracker:
    '''
    Responsiable to track the order of the events which they occured.
    '''
    def __init__(self) -> None:
        self.__event_map: Mapping[event, chronological_event_node] = {}
        self.__starting_node = chronological_event_node(event=None)
        self.__last_event_node = self.__starting_node
        self.__last_events = []

    def event_happend(self, event: event):
        self.__last_events.append(event)
        node: chronological_event_node
        if event in self.__event_map:
            node = self.__event_map[event]
        else:
            node = chronological_event_node(event=event)
            self.__event_map[event] = node
        self.__last_event_node.add_next(node)
        self.__last_event_node = node

    def __get_last_events(self):
        return self.__last_events
    
    def start_new_session(self):
        '''
        Delete the short term memmory and return all the short term memmories.
        '''
        self.__last_events = []
        self.__last_event_node = self.__starting_node
        return self.__get_last_events()

    def get_next_events(self, event: event):
        '''
        Return all the events that use to happend after this event
        '''
        if event not in self.__event_map:
            return None
        return list(map(lambda node: node.get_event(), self.__event_map[event].get_next_nodes()))
        
        
