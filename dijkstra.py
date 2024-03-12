from queue import PriorityQueue
from typing import Dict, List, Tuple
from datastructures import Graph, Node, Edge
from datetime import datetime as dt, timedelta as td
class Dijkstra:
    def __init__(self, graph: Graph, start_stop: str, end_stop: str, start_time: str) -> None:#todo jeszcze parametr czy czas czy przesiadki
        if start_stop not in graph.nodes.keys() or end_stop not in graph.nodes.keys():
            return 
        graph.nodes[start_stop].cost = 0
        self.original_graph: Graph = graph
        self.nodes_left: Dict[str, Node] = graph.nodes
        self.nodes_processed: Dict[str, Node] = {}
        # self.nodes_queue = PriorityQueue()
        # self.nodes_queue.put((0, self.nodes_left.pop(start_stop)))
        self.start_stop_name: str = start_stop
        self.end_stop_name: str = end_stop
        self.start_time: dt = dt.strptime(start_time, '%H:%M')
        # self.start_algorithm()
    
    def start_algorithm(self):
        current_node: Node
        current_node = self.nodes_left.pop(self.start_stop_name)#: Tuple[int, Node] 
        while current_node is not None and current_node.name != self.end_stop_name:
            self.nodes_processed[current_node.name] = current_node
            current_time = self.start_time + td(minutes=current_node.cost)
            node_edges: List[Edge] = self.original_graph.nodes_with_edges[current_node.name]
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

        print('Koniec Dijkstry')
        print(f'Całkowity koszt: {current_node.cost}')
        result = []
        while current_node.name != self.start_stop_name:
            result.insert(0,current_node.edge)
            current_node = current_node.edge.start_stop
        
        for edge in result:
            print(edge)