from .event import event
from typing import List
from dataclasses import dataclass

class node:
    def __init__(self, intensity: int, event: event) -> None:
        self.__intensity = intensity
        self.__event = event
        self.__edges: List["directed_edge"] = []

    def get_event(self):
        return self.__event
    
    def get_edge(self, n: int):
        return self.__edges[n]
    
    def get_intensity(self):
        return self.__intensity
    
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
    
    def connect_to_node(self, node: "node", strengrh: int):
        edge = directed_edge(next=node, strength=strengrh)
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


@dataclass
class directed_edge:
    next: node
    strength: int