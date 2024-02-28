from .event import event
from .chronological_event_tracker import chronological_event_tracker
from .memory_storage import memory_storage
from .event_supplier import event_supplier
from typing import *

    
class memory_manager:
    def __init__(self, event_supplier: event_supplier) -> None:
        self.__memories = memory_storage()
        self.__chronological_event_tracker = chronological_event_tracker()
        self.__event_supplier = event_supplier
        self.__seperator_type = self.__event_supplier.get_seperator_type()
        

    def absurb(self):
        while True:
            new_event: event
            try:
                new_event = self.__event_supplier()
            except event_supplier.end_of_events_exception:
                break
            if isinstance(new_event, self.__seperator_type):
                memory = \
                    self.__chronological_event_tracker.create_new_memory(new_event, intensity=new_event.get_intensity())
                self.__memories.add_memory(memory)
            else:
                self.__chronological_event_tracker.event_happend(event=new_event)