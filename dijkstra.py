from queue import PriorityQueue
from typing import Dict, List, Tuple
from datastructures import Graph, Node, Edge
from datetime import datetime as dt, timedelta as td
class Dijkstra:
    def __init__(self, graph: Graph, first_stop_name: str, last_stop_name: str, start_time: str, print_result: bool = True) -> None:
        if first_stop_name not in graph.nodes.keys() or last_stop_name not in graph.nodes.keys():
            return 
        graph.nodes[first_stop_name].cost = 0
        self.original_graph: Graph = graph
        self.nodes_left: Dict[str, Node] = graph.nodes.copy()
        self.nodes_processed: Dict[str, Node] = {}
        self.first_stop_name: str = first_stop_name
        self.last_stop_name: str = last_stop_name
        self.start_time: dt = dt.strptime(start_time, '%H:%M')
        self.print_result: bool = print_result
    
    def start_algorithm(self):
        current_node: Node
        current_node = self.nodes_left.pop(self.first_stop_name)#: Tuple[int, Node] 
        while current_node is not None and current_node.name != self.last_stop_name:
            self.nodes_processed[current_node.name] = current_node
            current_time = self.start_time + td(minutes=current_node.cost)
            # node_edges: List[Edge] = self.original_graph.nodes_with_edges[current_node.name]
            node_edges: List[Edge] = self.original_graph.get_node_edges_after_time(current_node.name, current_time)
            for edge in node_edges:
                #aktualizuj koszt -> aktualny koszt + czas potrzebny na przejazd + ile do odjazdu
                #i dodaj do kolejki 
                current_cost = current_node.cost + edge.calculate_edge_cost(current_time)
                if current_cost < edge.end_stop.cost:
                    edge.end_stop.cost = current_cost
                    edge.end_stop.edge = edge
            lowest_cost: int = float('inf')
            lowest_cost_stop: str = ''
            for stop in self.nodes_left.keys():
                if self.nodes_left[stop].cost < lowest_cost:
                    lowest_cost = self.nodes_left[stop].cost
                    lowest_cost_stop = stop
            if self.nodes_left.keys() != []:
                current_node = self.nodes_left.pop(lowest_cost_stop)
            else:
                current_node = None

        if self.print_result:
            print('Koniec Dijkstry')
            print(f'Całkowity koszt: {current_node.cost}')
            result = []
            while current_node.name != self.first_stop_name:
                result.insert(0,current_node.edge)
                current_node = current_node.edge.start_stop
            
            for edge in result:
                print(edge)