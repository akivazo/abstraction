from .event import event, seperator
from .event_supplier import event_supplier, event_supplier_impl
from typing import List
from .memory_manager import memory_manager


class missign_next_event_exception(Exception):
    def __init__(self, event: List[event]) -> None:
        self.event = event
        super().__init__(str(event))

class abstraction:
    
    def __init__(self, event_supplier : event_supplier):
        self.__memory = memory_manager(event_supplier=event_supplier)
        next_layer_event_supplier = event_supplier.get_next_layer_event_supplier()
        if next_layer_event_supplier is None:
            next_layer_event_supplier = event_supplier_impl()
        self.__next_layer_event_supplier = next_layer_event_supplier
        self.__next_layer: abstraction = None
        
    def __propagate_to_next_layer(self, event: event):
        self.__next_layer_event_supplier.add_event(event)
    
    def start(self):
        self.__memory.absurb()
        

    def __start_next_layer_learning(self):
        if self.__next_layer_event_supplier.get_non_processed_events_count() > 1:
            if self.__next_layer is None:
                self.__next_layer = \
                    __class__(event_supplier=self.__next_layer_event_supplier)
            self.__next_layer.learn()
            
    
    
    def get_strongest_next_event(self, event: event):
        events = self.__chronological_event_tracker.get_next_events(event=event)
        if events is None or len(events) == 0:
            raise missign_next_event_exception(event=event)
        return max(events, key=self.get_events_intensity)
    
    def get_events_intensity(self, event: event):
        return self. __events_intensity_tracker.get_event_intensity(event)
    
    def __procces_events(self, events: List[event]):
        assert events
        if len(question.get_events()) == 1:
            single_event = question.pop(0)
            return [self.__known_events_tracker.find_closest_known_event(single_event)]
        return list(map(self.__known_events_tracker.find_closest_known_event, question))
    
    def __split_by_seperator(self, events: List[event], seperator: seperator):
        splitted_list = []
        current_list = []
        current_item = None
        while len(events) > 0:
            current_item = events.pop(0)
            if current_item is seperator:
                if len(current_list) == 0:
                    continue
                splitted_list.append(current_list)
                current_list = []
            else:
                current_list.append(current_item)
        if len(current_list) > 0:
            # in case there isn't seperator in the end
            splitted_list.append(current_list)
        return splitted_list

    def responde(self, events: List[event]):
        events = self.__procces_events(question)
        splitted_events = self.__split_by_seperator(events=events, seperator=self.__seperator)
        big_events = list(map(event.merge_events, splitted_events))
        if self.__next_layer is None:
            last_event = big_events.pop()
            return self.get_strongest_next_event(last_event)
        return self.__next_layer.responde(big_events)



        
        



            
    
                