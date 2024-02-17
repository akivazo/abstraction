from .node import node, fake_node
from .event import event, eof_event, event_supplier, event_supplier_impl, end_of_big_event
from typing import List, Mapping, Set
import sys


class abstraction:
    def __init__(self, event_supplier : event_supplier):
        self.__nodes: List[node] = []
        self.__event_map: Mapping[event, node] = {}
        self.__event_supplier = event_supplier
        self.__last_nodes: List[node] = []
        self.__next_layer_event_supplier = event_supplier_impl()
        self.__next_layer: abstraction = None
        self.__next_layer_events = []


    def __get_event_intentsity(self, event: event):
        return event.intensity

    def __create_node(self, event: event):
        new_node = node(event=event)
        self.__add_node(new_node)
        return new_node

    def __add_node(self, new_node: node):
        self.__nodes.append(new_node)
        self.__event_map[new_node.get_event()] = new_node
        return new_node
        
    
    def __propagate_to_next_layer(self, node: node):
        if self.__next_layer is None:
            self.__next_layer = abstraction(self.__next_layer_event_supplier)
        event = node.get_event()
        self.__next_layer_events.append(event)
        self.__next_layer_event_supplier.add_event(event)

    def __merge_last_events(self):
        merged_node = sum(self.__last_nodes, start=fake_node())
        return None if isinstance(merged_node, fake_node) else merged_node
    
    def __get_last_node_created(self):
        try:
            return self.__last_nodes[-1]
        except IndexError:
            return None
    
    def process(self, event: event): 
        new_node: node
        last_node = self.__get_last_node_created()
        try:
            new_node = self.__event_map[event]
            new_node.increase_intensity(self.__get_event_intentsity(event))
        except KeyError:
            new_node = self.__create_node(event)
        self.__last_nodes.append(new_node)
        if last_node is not None:
            last_node.connect_to_node(node=new_node)

    def learn(self):
        while True:
            new_event = self.__event_supplier()
            if new_event is None:
                raise Exception("event shouldent be None")
            if isinstance(new_event, end_of_big_event):
                merged_event_node = self.__merge_last_events()
                if merged_event_node is not None:
                    self.__propagate_to_next_layer(merged_event_node)
                self.__last_nodes = []
                if isinstance(new_event, eof_event):
                    if self.__next_layer is not None and len(self.__next_layer_events) > 1:
                        self.__next_layer.learn()
                    break
            else:
                self.process(new_event)
            
    def get_events_count(self):
        return len(self.__nodes)
    
    def is_there_is_next_abstraction(self):
        return self.__next_layer is not None and \
            self.__next_layer.get_events_count() > 1
        

    def show_abstraction(self, depth: int=sys.maxsize):
        if depth == 0 or not self.is_there_is_next_abstraction():
            return list(map(lambda node: node.get_event(), self.__nodes))
        return self.__next_layer.show_abstraction(depth=depth - 1)
        
        



            
    
                