from .event import event, eof_event
from typing import List
from dataclasses import dataclass

class node:
    class not_enough_edges_exception(Exception):
        def __init__(self, n, edges_num) -> None:
            super().__init__(f"This node has '{edges_num}'. requested edge index '{n}'")
    def __init__(self, event: event) -> None:
        self.__intensity = event.intensity
        self.__event = event
        self.__edges: List["directed_edge"] = []
    
    def get_edge(self, n: int):
        return self.__edges[n]
    
    def get_intensity(self):
        return self.__intensity
    
    def get_event(self):
        return self.__event
    
    def add_edge(self, edge):
        self.__edges.append(edge)

    def decrease_instensity(self):
        self.__intensity -= 1

    def is_alive(self):
        return self.__intensity > 0
    
    def is_dead(self):
        return not self.is_alive()
    
    def get_rank(self):
        return len(self.__edges)
    
    def connect_to_node(self, node: "node"):
        edge = directed_edge(next=node)
        self.__edges.append(edge)

    def search_event(self, event: "event"):
        for edge in self.__edges:
            next_node = edge.next
            if event == next_node.__event:
                return next_node
        return None
    
    def increase_intensity(self, intensity):
        self.__intensity += intensity

    def get_strongest_connection(self):
        return max(self.__edges, key=lambda edge: edge.strength, default=None)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.get_event().__repr__(), self.get_intensity()
    
    def __add__(self, other: "node"):
        next_node = other.get_edge(0).next
        new_event = self.get_event() + other.get_event()
        new_node = node(event=new_event)
        new_node.connect_to_node(next_node)
        return new_node
    
    def __hash__(self):
        return self.get_event().__hash__()
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, node):
            return self.__hash__() == __value.__hash__()
        return False

class eof_node(node):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(eof_node, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def __init__(self) -> None:
        self.__intensity = 0

    def __add__(self, other):
        return other
    
    def increase_intensity(self, intensity):
        pass

    def get_rank(self):
        return 0
    
    def get_intensity(self):
        return 0
    
    def get_event(self):
        return eof_event()
    

@dataclass
class directed_edge:
    next: node