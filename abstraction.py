from .node import node, directed_edge
from .event import event, eof_event
from typing import List, Mapping, Callable, Set
from weakref import WeakSet


class abstraction:
    def __init__(self, event_supplier :Callable[[], event]):
        self.__nodes: Set[node] = WeakSet()
        self.__event_map: Mapping[event, node] = {}
        self.__live_nodes: Set[node] = WeakSet()
        self.__event_supplier: Callable[[], event] = event_supplier
        self.__last_node = None


    def get_event_intentsity(self, event: event):
        return event.intensity

    def create_node(self, event: event):
        new_node = node(intensity=self.get_event_intentsity(event), event=event)
        self.__nodes.add(new_node)
        self.__event_map[event] = new_node
        self.__last_node = new_node
        self.__live_nodes.add(new_node)
        return new_node

    def start_intensity_count_down(self, node: node):
        self.__live_nodes.add(node)

    def get_last_node_created(self):
        return self.__last_node

    def add_new_leaf_node(self, node: node):
        pass

    def get_node_intensity(self, node: node):
        return node.get_intensity()

    def connect_to_node(self, node_to_connetct_to: node, node: node, connection_strngth):
        new_edge = directed_edge(source=node, target=node_to_connetct_to, strength=connection_strngth)
        node.add_edge(new_edge)

    def is_all_events_warm_out(self):
        return len(self.__live_nodes) == 0

    def is_part_of_branch(self, node: node):
        return node.get_rank() == 1
    
    def __merge_nodes(self, node1: node, node2: node):
        next_node = node2.get_edge(0).next
        new_event = node1.get_event() + node2.get_event()
        new_node = self.create_node(new_event)
        new_node.connect_to_node(next_node, strengrh=node1.get_intensity() + node2.get_intensity())
        return new_node

    def __find_branch(self, node: node):
        branch_node = None
        old_nodes = set()
        if self.is_part_of_branch(node):
            old_nodes.add(node)
            branch_node = node
            next_node = node.get_edge(0).next
            rest_of_branch_node, rest_of_branch_old_nodes = self.__find_branch(next_node)
            if rest_of_branch_node is not None:
                branch_node = self.__merge_nodes(node, rest_of_branch_node)
                old_nodes = old_nodes.union(rest_of_branch_old_nodes)
        return branch_node, old_nodes
    
    def summarize_isolated_branches(self):
        def aux(branches_parts_nodes):
            if not branches_parts_nodes:
                return []
            part_of_branch_node = branches_parts_nodes[0]
            branch_node, old_nodes = self.__find_branch(part_of_branch_node)
            branches_parts_nodes -= old_nodes
            return [branch_node] + aux(branches_parts_nodes)

        branches_parts_nodes = list(filter(self.is_part_of_branch, self.__nodes))
        branches_nodes: List[node] = aux(branches_parts_nodes)
        self.__nodes.union(branches_nodes)
        for branch_node in branches_nodes:
            self.process(branch_node.get_event())

    def tik(self):
        nodes_to_remove = set()
        for node in self.__live_nodes:
            node.decrease_instensity()
            if node.is_dead():
                nodes_to_remove.add(node)
        self.__live_nodes.difference_update(nodes_to_remove)
        if self.is_all_events_warm_out():
            self.summarize_isolated_branches()
            self.__last_node = None

    def process(self, event: event): 
        new_node: node
        try:
            new_node = self.__event_map[event]
        except KeyError:
            new_node = self.create_node(event)
        last_node = self.get_last_node_created()
        if last_node is not None:
            last_node.connect_to_node(node=new_node, strengrh=self.get_node_intensity(new_node))

    def learn(self):
        while True:
            new_event = self.__event_supplier()
            if isinstance(new_event, eof_event) or new_event is None:
                break
            self.process(new_event)
            self.tik()

    def get_evevnts_abstraction(self, events: List[event]):
        current_node = self.__default_node
        while len(events) > 0:
            event = events.pop(0)
            current_node = current_node.search_event(event)
            if current_node is None:
                return None
        return current_node.get_strongest_connection().next.get_event()
        



            
    
                