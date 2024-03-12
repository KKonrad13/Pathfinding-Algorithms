from datastructures import *
from dijkstra import Dijkstra
# FILE_PATH = 'connection_graph_A_line.csv'
FILE_PATH = 'connection_graph.csv'


if __name__=='__main__':#todo obsluzyc przypadek gdy przystanek nie istnieje
    graph = Graph(FILE_PATH)
    # dijkstra = Dijkstra(graph, 'Bezpieczna', 'Czajkowskiego', '12:22')
    # dijkstra = Dijkstra(graph, 'Katedra', 'Kadłubka', '12:22')
    dijkstra = Dijkstra(graph, 'Nowowiejska', 'PL. GRUNWALDZKI', '12:22')
    dijkstra.start_algorithm()
