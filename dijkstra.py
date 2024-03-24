from queue import PriorityQueue
from typing import Dict, List, Tuple
from datastructures import Graph, Node, Edge
from datetime import datetime as dt, timedelta as td
class Dijkstra:
    def __init__(self, graph: Graph) -> None:
        self.original_graph: Graph = graph
        self.reset_graph()
    
    def configure_variables(self, first_stop: str, last_stop: str, start_time: str, print_result: bool):
        if first_stop not in self.original_graph.nodes.keys() or last_stop not in self.original_graph.nodes.keys():
            return False 
        self.first_stop_name: str = first_stop
        self.last_stop_name: str = last_stop
        self.last_stop: Node = self.nodes_left[last_stop]
        start_h, start_m = map(int, start_time.split(':'))
        start_dt = dt.strptime(f'{(start_h%24):02d}:{start_m:02d}', '%H:%M')
        if start_h >= 24:
            start_dt += td(hours=24)
        self.start_time: dt = start_dt
        return True
    

    def reset_graph(self):
        self.nodes_left: Dict[str, Node] = self.original_graph.nodes.copy()
        for name in self.nodes_left:
            self.nodes_left[name].cost = float('inf')
            self.nodes_left[name].edge = None
        self.nodes_processed: Dict[str, Node] = {}


    def start_algorithm(self, first_stop: str, last_stop: str, start_time: str, print_result: bool = True) -> Node:
        self.reset_graph()
        if not self.configure_variables(first_stop, last_stop, start_time, print_result):
            return None

        current_node: Node
        current_node = self.nodes_left.pop(self.first_stop_name)
        current_node.cost = 0
        while current_node is not None and current_node.name != self.last_stop_name:
            self.nodes_processed[current_node.name] = current_node
            current_time = self.start_time + td(minutes=current_node.cost)
            node_edges: List[Edge] = self.original_graph.get_node_edges_after_time(current_node.name, current_time)
            for edge in node_edges:
                #aktualizuj koszt -> aktualny koszt + czas potrzebny na przejazd + ile do odjazdu
                #i dodaj do kolejki 
                current_cost = current_node.cost + edge.calculate_edge_cost(current_time)
                if current_cost < edge.end_stop.cost:
                    edge.end_stop.cost = current_cost
                    edge.end_stop.edge = edge
                    
            lowest_cost_stop: str = self.get_lowest_cost_stop_name()
            
            if lowest_cost_stop != '' and self.nodes_left.keys() != []:
                current_node = self.nodes_left.pop(lowest_cost_stop)
            else:
                current_node = None

        if not current_node and print_result:
            time_diff: td = self.start_time - dt(1900, 1, 1, 0, 0, 0)
            hours = time_diff.total_seconds() // 3600
            minutes = (time_diff.total_seconds() % 3600) // 60
            print(f'Nie znaleziono ścieżki dla połacznia {self.first_stop_name} -> {self.last_stop_name} rozpoczynającego się o godzinie {int(hours):02d}:{int(minutes):02d}')
        elif print_result:
            self.print_result(current_node)
        return current_node

    def get_lowest_cost_stop_name(self):
        lowest_cost_stop: str = ''
        lowest_cost: int = float('inf')
        for stop in self.nodes_left.keys():
            stop_whole_cost = self.nodes_left[stop].cost + self.nodes_left[stop].heuristic_cost
            if stop_whole_cost < lowest_cost:
                lowest_cost = stop_whole_cost
                lowest_cost_stop = stop
        return lowest_cost_stop

    def print_result(self, current_node: Node):
        print('Koniec Dijkstry')
        print(f'Całkowity koszt: {current_node.cost}')
        result = []
        while current_node.name != self.first_stop_name:
            result.insert(0,current_node.edge)
            current_node = current_node.edge.start_stop
        
        for edge in result:
            print(edge)