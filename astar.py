from typing import Dict, List
from datastructures import Graph, Node, Edge
from datetime import datetime as dt, timedelta as td
class Astar:
    def __init__(self, graph: Graph, fisrt_stop: str, last_stop: str, start_time: str, print_result: bool = True) -> None:#todo jeszcze parametr czy czas czy przesiadki
        if fisrt_stop not in graph.nodes.keys() or last_stop not in graph.nodes.keys():
            return 
        graph.nodes[fisrt_stop].cost = 0
        self.original_graph: Graph = graph
        self.nodes_left: Dict[str, Node] = graph.nodes.copy()
        self.nodes_processed: Dict[str, Node] = {}
        self.fisrt_stop_name: str = fisrt_stop
        self.last_stop_name: str = last_stop
        self.last_stop: Node = self.nodes_left[last_stop]
        self.start_time: dt = dt.strptime(start_time, '%H:%M')
        self.print_result: bool = print_result
    
    def start_algorithm(self):
        current_node: Node
        current_node = self.nodes_left.pop(self.fisrt_stop_name)
        while current_node is not None and current_node.name != self.last_stop_name:
            self.nodes_processed[current_node.name] = current_node
            current_time = self.start_time + td(minutes=current_node.cost)
            node_edges: List[Edge] = self.original_graph.get_node_edges_after_time(current_node.name, current_time)
            for edge in node_edges:
                #aktualizuj koszt -> aktualny koszt + czas potrzebny na przejazd + ile do odjazdu
                #i dodaj do kolejki 
                self.calculate_costs_TIME_CONDITION(current_node, edge, current_time)
            lowest_cost_stop: str = self.get_lowest_cost_stop_name()
            
            if self.nodes_left.keys() != []:
                current_node = self.nodes_left.pop(lowest_cost_stop)
            else:
                current_node = None

        if self.print_result:
            self.print_result(current_node)
    
    def calculate_costs_TIME_CONDITION(self, current_node: Node, edge: Edge, current_time: dt):
        current_time_cost = current_node.cost + edge.calculate_edge_cost(current_time)
        current_heuristic_cost = 500 * edge.calculate_astar_heuristic_euklides_cost(self.last_stop.lat, self.last_stop.lon)
        whole_cost = current_time_cost + current_heuristic_cost
        if whole_cost < edge.end_stop.cost + edge.end_stop.heuristic_cost:
            edge.end_stop.cost = current_time_cost
            edge.end_stop.heuristic_cost = current_heuristic_cost
            edge.end_stop.edge = edge

    def calculate_costs_BUS_CHANGE_CONDITION(self, current_node: Node, edge: Edge):
        current_bus_change_cost = current_node.cost + 0 if edge.is_previous_edge(current_node.edge) else 1
        current_heuristic_cost = 500 * edge.calculate_astar_heuristic_euklides_cost(self.last_stop.lat, self.last_stop.lon)


    def get_lowest_cost_stop_name(self):
        lowest_cost_stop: str = ''
        lowest_cost: int = float('inf')
        for stop in self.nodes_left.keys():
            stop_whole_cost = self.nodes_left[stop].cost + self.nodes_left[stop].heuristic_cost
            if stop_whole_cost < lowest_cost:
                lowest_cost = stop_whole_cost
                lowest_cost_stop = stop
        return lowest_cost_stop

    def print_result(self, current_node):
        print('Koniec A*')
        print(f'Całkowity koszt: {current_node.cost}')
        result = []
        while current_node.name != self.fisrt_stop_name:
            result.insert(0,current_node.edge)
            current_node = current_node.edge.start_stop
        
        for edge in result:
            print(edge)