from .event import event
from typing import List, Mapping
from dataclasses import dataclass
from .event_intensity_tracker import events_intensity_tracker

@dataclass
class dont_know:
    known_events: List[event]
    unknown_events: List[event]

class event_node:
    def __init__(self, event: event) -> None:
        self.__event = event
        self.__next: Mapping[event, "event_node"] = {}

    def get_next_nodes(self) -> List["event_node"]:
        return list(self.__next.keys())
    
    def add_next(self, node: "event_node"):
        self.__next[node.get_event()] = node

    def get_event(self):
        return self.__event

    def get_next_event_node(self, next_event: event):
        try:
            return self.__next[next_event]
        except KeyError:
            return None

class known_events_tracker:
    '''
    Responsiable to remember all the events that happend,
    and find closest known event to an unknown event.
    '''
    def __init__(self, events_intensity_tracker: events_intensity_tracker) -> None:
        self.__internals_events_starting_node = event_node(None)
        self.__events = set()
        self.__events_intensity_tracker = events_intensity_tracker

    def add_event(self, event: event):
        internal_events = event.get_internal_events()
        current_node = self.__internals_events_starting_node
        self.__events.add(event)
        while len(internal_events) > 0:
            internal_event = internal_events.pop(0)
            next_node = current_node.get_next_event_node(internal_event)
            if next_node is None:
                next_node = event_node(internal_event)
                current_node.add_next(next_node)
            current_node = next_node

    def __get_node_intensity(self, node: event_node):
        return self.__events_intensity_tracker(node.get_event())
    
    def find_closest_known_event(self, event_inst: event):
        if event_inst in self.__events:
            return event_inst
        internal_events = event_inst.get_internal_events()
        current_node = self.__internals_events_starting_node
        distance = 0
        known_internal_events = []
        while len(internal_events) > 0:
            internal_event = internal_events.pop(0)
            next_node = current_node.get_next_event_node(internal_event)
            if next_node is None:
                next_nodes = current_node.get_next_nodes()
                if len(next_nodes) == 0:
                    unknown_events = [internal_event] + internal_events
                    return dont_know(known_events=known_internal_events, unknown_events=unknown_events)
                next_node = max(next_nodes, key=self.__get_node_intensity)
                distance += 1
            known_internal_events.append(next_node.get_event())
            current_node = next_node
        if len(known_internal_events) == 0:
            return None
        return event.merge_events(known_internal_events)
        
