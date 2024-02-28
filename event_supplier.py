from typing import *
from abc import abstractmethod, ABC
from .event import event, seperator

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
    def get_seperator_type(self) -> Type[seperator]:
        '''
        Return the seperator type for the current layer.
        The seperator should be used to seperate between meaninful groups of events. 
        e.g. dot in the end of a sentence to seperate between words.
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
        self.__seperator_type = None
        self.__next_layer_event_supplier = None
        if len(seperators) > 0:
            self.__seperator = seperators.pop(0)
            self.__next_layer_event_supplier = __class__(seperators=seperators)

    def get_next_layer_event_supplier(self) -> event_supplier:
        return self.__next_layer_event_supplier
    
    def add_event(self, event: event):
        self.__events_queue.append(event)

    def get_events(self):
        return self.__events_queue

    def get_non_processed_events_count(self):
        return len(self.__events_queue)
    
    def get_seperator_type(self) -> seperator:
        return self.__seperator
    
    def __call__(self):
        if len(self.__events_queue) > 0:
            return self.__events_queue.pop(0)
        raise event_supplier.end_of_events_exception()

