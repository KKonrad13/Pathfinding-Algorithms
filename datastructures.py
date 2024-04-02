import csv
from typing import Dict, List
from datetime import datetime as dt, timedelta as td
from math import sqrt, pow
class Node:
    def __init__(self, name: str, lat: str, lon: str) -> None:
        self.name = name
        self.lat: float = float(lat)
        self.lon: float = float(lon)
        self.cost: int = float('inf')
        self.heuristic_cost: float = 0
        self.edge: Edge = None #przy inicjalizacji nie mamy ścieżki

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Node) and self.name == __value.name 
    
    
class Edge:
    def __init__(self, line: str, departure_time: dt, arrival_time: dt, start_stop: Node, end_stop: Node) -> None:
        time_diff = arrival_time - departure_time
        self.time_cost: int = time_diff.total_seconds() // 60
        self.line: str = line
        self.departure: dt = departure_time
        self.arrival: dt = arrival_time
        self.start_stop: Node = start_stop
        self.end_stop: Node = end_stop

    def __hash__(self) -> int:
        return hash(self.line + self.start_stop.name + self.end_stop.name)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Edge):
            return False
        same_stops =  self.start_stop.name == __value.start_stop.name and self.end_stop.name == __value.end_stop.name
        return self.line == __value.line and same_stops 
    
    def __str__(self) -> str:
        min_dt: dt = dt(1900, 1, 1, 0, 0, 0)
        dep_time_diff: td = self.departure - min_dt
        arr_time_diff: td = self.arrival - min_dt
        dep_h = dep_time_diff.total_seconds() // 3600
        dep_m = (dep_time_diff.total_seconds() % 3600) // 60  
        arr_h = arr_time_diff.total_seconds() // 3600
        arr_m = (arr_time_diff.total_seconds() % 3600) // 60  
        return f'Linia: {self.line}, {self.start_stop.name} -> {self.end_stop.name}, {int(dep_h):02d}:{int(dep_m):02d} -> {int(arr_h):02d}:{int(arr_m):02d}'

    def calculate_edge_cost(self, current_time: dt):
        time_diff = self.departure - current_time
        #zwracamy czas przejazdu + ile musimy czekać na przystanku
        return self.time_cost + time_diff.total_seconds() // 60
    
    def calculate_astar_heuristic_manhattan_cost(self, last_stop_lat: float, last_stop_lon: float):
        return abs(last_stop_lat - self.end_stop.lat) + abs(last_stop_lon - self.end_stop.lon)
    
    def calculate_astar_heuristic_euklides_cost(self, last_stop_lat: float, last_stop_lon: float):
        return sqrt(pow((last_stop_lat - self.end_stop.lat), 2) + pow((last_stop_lon - self.end_stop.lon), 2))

    def is_previous_edge_or_none(self, other_edge):#TODO czemu nie moge :Edge
        return other_edge is None or (self.departure == other_edge.arrival and self.line == other_edge.line)

class Graph:
    def __init__(self, file_path) -> None:
        self.nodes: Dict[str, Node] = {}
        self.nodes_with_edges: Dict[str, List[Edge]] = {}
        self.edges: List[Edge] = []
        self.read_graph_from_csv(file_path)
    
    def read_graph_from_csv(self, file_path):
        index_line = 2
        index_departure_time = 3
        index_arrival_time = 4
        index_start_stop = 5
        index_end_stop = 6
        index_start_stop_lat = 7
        index_start_stop_lon = 8
        index_end_stop_lat = 9
        index_end_stop_lon = 10
        with open(file_path, encoding="UTF-8") as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for line in reader:
                start_stop_name = line[index_start_stop]
                end_stop_name = line[index_end_stop]
                if start_stop_name not in self.nodes.keys():
                    self.nodes[start_stop_name] = Node(start_stop_name, line[index_start_stop_lat], line[index_start_stop_lon])
                if end_stop_name not in self.nodes.keys():
                    self.nodes[end_stop_name] = Node(end_stop_name, line[index_end_stop_lat], line[index_end_stop_lon])
                
                start_stop = self.nodes[start_stop_name]
                end_stop = self.nodes[end_stop_name]
                
                dep_h, dep_m, _ = map(int, line[index_departure_time].split(':'))
                arr_h, arr_m, _ = map(int, line[index_arrival_time].split(':'))
                dep_dt = dt.strptime(f'{(dep_h%24):02d}:{dep_m:02d}', '%H:%M')
                arr_dt = dt.strptime(f'{(arr_h%24):02d}:{arr_m:02d}', '%H:%M')
                if dep_h >= 24:
                    dep_dt += td(hours=24)
                if arr_h >= 24:
                    arr_dt += td(hours=24)  
                edge = Edge(line[index_line], dep_dt, arr_dt, start_stop, end_stop)
                if start_stop_name not in self.nodes_with_edges.keys():
                    self.nodes_with_edges[start_stop_name] = [edge]
                else:
                    self.nodes_with_edges[start_stop_name].append(edge)

                #dla przypadku gdy przystanek nie ma żadnych sąsiadów - i tak chcemy, żeby jego nazwa była w słowniku
                if end_stop_name not in self.nodes_with_edges.keys():
                    self.nodes_with_edges[end_stop_name] = []

                self.edges.append(edge)
    
    def get_node_edges_after_time(self, stop_name: str, time: dt):
        # return filter(lambda edge: edge.departure >= time , self.nodes_with_edges[stop_name]) 
        return sorted(filter(lambda edge: edge.departure >= time, self.nodes_with_edges[stop_name]), key=lambda edge: edge.departure) 
    