from .event import event, event_supplier, event_supplier_impl
from .known_event_tracker import known_events_tracker, dont_know
from .chronological_event_tracker import chronological_event_tracker
from .event_intensity_tracker import events_intensity_tracker
from typing import List

class unknown_events_exception(Exception):
    def __init__(self, known_events: List[event], unknown_events: List[event]) -> None:
        self.known_events = known_events
        self.unknown_events = unknown_events

class missign_next_event_exception(Exception):
    def __init__(self, event: List[event]) -> None:
        self.event = event

class abstraction:
    
    def __init__(self, event_supplier : event_supplier):
        self.__events_intensity_tracker = events_intensity_tracker()
        self.__chronological_event_tracker = chronological_event_tracker()
        self.__known_events_tracker = known_events_tracker(self.__events_intensity_tracker)
        self.__event_supplier = event_supplier
        next_layer_event_supplier = event_supplier.get_next_layer_event_supplier()
        if next_layer_event_supplier is None:
            next_layer_event_supplier = event_supplier_impl()
        self.__next_layer_event_supplier = next_layer_event_supplier
        self.__next_layer: abstraction = None
        self.__seperator = self.__event_supplier.get_seperator()
        
    def __propagate_to_next_layer(self, event: event):
        self.__next_layer_event_supplier.add_event(event)
    
    def process(self, event: event, intensity: int): 
        self.__chronological_event_tracker.event_happend(event=event)
        self.__known_events_tracker.add_event(event=event)
        self.__events_intensity_tracker.add_event(event=event, intensity=intensity)

    def __start_next_layer_learning(self):
        if self.__next_layer is None:
            self.__next_layer = \
                __class__(event_supplier=self.__next_layer_event_supplier)
        if self.__next_layer_event_supplier.get_non_processed_events_count() > 1:
            self.__next_layer.learn()
            
    def learn(self):
        while True:
            new_event: event
            try:
                new_event, intensity = self.__event_supplier()
                if not isinstance(new_event, event):
                    raise Exception(f"Events should from type '{type(event)}', got '{type(new_event)}.")
            except event_supplier.break_exception:
                self.__start_next_layer_learning()
                continue
            except event_supplier.end_of_events_exception:
                self.__start_next_layer_learning()
                break
            if new_event is self.__seperator:
                last_events = self.__chronological_event_tracker.start_new_session()
                merged_event = event.merge_events(last_events)
                if merged_event is not None:
                    self.__propagate_to_next_layer(merged_event)
            else:
                self.process(new_event, intensity=intensity)

    def get_events_intensity(self, event: event):
        return self. __events_intensity_tracker.get_event_intensity(event)
    
    def answer(self, events: List[event]):
        if len(events) == 1:
            single_event = events.pop(0)
            closest_event = self.__known_events_tracker.find_closest_known_event(single_event)
            if isinstance(closest_event, dont_know):
                raise unknown_events_exception(known_events=closest_event.known_events,
                                                unknown_events=closest_event.unknown_events)
            events = self.__chronological_event_tracker.lget_next_events(event=closest_event)
            if events is None or len(events) == 0:
                raise missign_next_event_exception(event=closest_event)
            return max(events, key=self.get_events_intensity)
        known_events = list(map(self.__known_events_tracker.find_closest_known_event, events))
        big_events = []
        for closest_event in known_events:
            big_event_events = []
            if closest_event is self.__seperator:
                big_event = event.merge_events(big_event_events)
                big_events.append(big_event)
                big_event_events = []
            else:
                big_event_events.append(closest_event)
        
        return self.__next_layer.answer(big_events)



        
        



            
    
                