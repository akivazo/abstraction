from .node import node, eof_node
from .event import event, eof_event, event_supplier, event_supplier_impl
from typing import List, Mapping, Set
import sys


class abstraction:
    def __init__(self, event_supplier : event_supplier):
        self.__nodes: List[node] = []
        self.__event_map: Mapping[event, node] = {eof_event(): eof_node()}
        self.__event_supplier = event_supplier
        self.__last_node = None
        self.__next_layer_event_supplier = event_supplier_impl()
        self.__next_layer: abstraction = None


    def __get_event_intentsity(self, event: event):
        return event.intensity

    def __create_node(self, event: event):
        new_node = node(event=event)
        self.__add_node(new_node)
        return new_node

    def __add_node(self, new_node: node):
        self.__nodes.append(new_node)
        self.__event_map[new_node.get_event()] = new_node
        self.__last_node = new_node
        return new_node

    def __get_last_node_created(self):
        return self.__last_node

    def __get_node_intensity(self, node: node):
        return node.get_intensity()

    def __is_part_of_branch(self, node: node):
        return node.get_rank() == 1
    
    def __merge_nodes(self, node1: node, node2: node):
        return node1 + node2
        

    def __propagate_to_next_layer(self, event):
        self.__next_layer_event_supplier.add_event(event)
        
    def __find_branch(self, node: node, visited: Set[node]):
        branch_node = None
        if self.__is_part_of_branch(node):
            branch_node = node
            next_node = node.get_edge(0).next
            if next_node in visited:
                return branch_node
            visited.add(next_node)
            rest_of_branch_node = self.__find_branch(next_node, visited=visited)
            if rest_of_branch_node is not None:
                branch_node = self.__merge_nodes(node, rest_of_branch_node)
        return branch_node
    
    def __summarize_isolated_branches(self):
        def aux(branches_parts_nodes: list):
            try:
                part_of_branch_node = branches_parts_nodes.pop(0)
            except IndexError:
                return []
            visited = set()
            branch_node = self.__find_branch(part_of_branch_node, visited=visited)
            branches_parts_nodes = [node for node in branches_parts_nodes if node not in visited]
            return [branch_node] + aux(branches_parts_nodes)

        branches_parts_nodes = list(filter(self.__is_part_of_branch, self.__nodes))
        branches_nodes: List[node] = aux(branches_parts_nodes)
        if len(branches_nodes) > 1:
            for branch_node in branches_nodes:
                self.__propagate_to_next_layer(branch_node.get_event())
            return True
        return False

    def merge_last_events(self):
        
    def process(self, event: event): 
        new_node: node
        last_node = self.__get_last_node_created()
        try:
            new_node = self.__event_map[event]
            new_node.increase_intensity(self.__get_event_intentsity(event))
        except KeyError:
            new_node = self.__create_node(event)
        if last_node is not None:
            last_node.connect_to_node(node=new_node)

    def learn(self):
        while True:
            new_event = self.__event_supplier()
            if new_event is None:
                raise Exception("event shouldent be None")
            self.process(new_event)
            if isinstance(new_event, eof_event):
                found_branches = self.__summarize_isolated_branches()
            if found_branches:
                self.__next_layer = abstraction(event_supplier=self.__next_layer_event_supplier)
                self.__next_layer.learn()
        

    def show_abstraction(self, depth: int=sys.maxsize):
        if depth == 0 or self.__next_layer is None:
            return list(map(lambda node: node.get_event(), self.__nodes))
        return self.__next_layer.show_abstraction(depth=depth - 1)
        
        



            
    
                