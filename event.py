from dataclasses import dataclass
from typing import Any, List, Tuple
from abc import abstractmethod, ABC


class event(ABC):
    '''
    override this class to create your custom event
    '''
    def __init__(self):
        self.__internal_events = [] # the events that used to create this event
        
    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, event):
            return self.__hash__() == __value.__hash__()
        return False

    @abstractmethod  
    def __add__(self, other: "event"):
        pass
    
    def get_internal_events(self):
        return self.__internal_events
    
    def set_internal_events(self, events: List["event"]):
        self.__internal_events = events

    @staticmethod
    def merge_events(events: List["event"]):
        merged_event = sum(events, start=fake_event())
        if isinstance(merged_event, fake_event):
            return None
        merged_event.set_internal_events(events)
        return merged_event
    


class fake_event(event):

    def __hash__(self) -> int:
        raise NotImplementedError()
    
    def __add__(self, other: event):
        return other

class seperator(fake_event):
    pass 

class event_supplier(ABC):
    @abstractmethod
    def __call__(self) -> Tuple[event, int]:
        '''
        Return an event and the 'intensity' which this event happend.
        The intensity used as a break even when there are multiple event candidates to chose from. 
        '''
        pass

    class break_exception(Exception):
        '''
        Should be used in the __call__ method after a significante amount of events or when 
        a methodology break is needed.
        '''
        pass

    class end_of_events_exception(Exception):
        '''
        Should be used in the __call__ method when there are no more events to supply.
        '''
        pass

    @abstractmethod
    def get_seperator(self) -> seperator:
        '''
        Return a seperator for the current layer.
        The seperator should be used to seperate between meaninful groups of events. (e.g. in the end of a sentence)
        The seperator should be the same objects as returned in the __call__ method.
        The 'is' keyword will be used to idenitfied the seperator against supplied event.
        '''
        pass

    @abstractmethod
    def get_next_layer_event_supplier(self) -> "event_supplier":
        '''
        Return an event_supplier that will be used in the next layer.
        The event_supplier for the next layer will be fed from the events 
        constructs in the current layer (using the 'add_event' method)
        '''
        pass

    @abstractmethod
    def add_event(self, event: event):
        pass

    @abstractmethod
    def get_non_processed_events_count(self):
        '''
        Return the events waiting to be supplied
        '''
        pass

class event_supplier_impl(event_supplier):
    def __init__(self, seperators: List[seperator]) -> None:
        self.__events_queue = []
        self.__seperator = None
        self.__next_layer_event_supplier = None
        if len(seperators) > 0:
            self.__seperator = seperators.pop(0)
            self.__next_layer_event_supplier = __class__(seperators=seperators)

    def get_next_layer_event_supplier(self) -> event_supplier:
        return self.__next_layer_event_supplier
    
    def add_event(self, event: event, intensity: int):
        self.__events_queue.append((event, intensity))

    def get_events(self):
        return self.__events_queue

    def get_non_processed_events_count(self):
        return len(self.__events_queue)
    
    def get_seperator(self) -> seperator:
        return self.__seperator
    
    def __call__(self) -> Any:
        if len(self.__events_queue) > 0:
            return self.__events_queue.pop(0)
        raise event_supplier.end_of_events_exception()

