from datastructures import *
from dijkstra import Dijkstra
from astar import Astar
import time
FILE_PATH = './ignore/connection_graph.csv'

class Test:
    def __init__(self, file_path) -> None:
        current_time = time.time()
        self.graph = Graph(file_path)
        self.simple_path = (self.graph, 'Nowowiejska', 'PL. GRUNWALDZKI', '12:22')
        self.medium_path = (self.graph, 'Bezpieczna', 'Czajkowskiego', '12:22')
        # self.long_path = (self.graph, 'Katedra', 'Kadłubka', '12:22')
        # self.long_path = (self.graph, 'Reja', 'Kadłubka', '25:59')#TODO ubsłużyć przypadek >24
        self.long_path = (self.graph, 'PETRUSEWICZA', 'Młodych Techników', '25:59')#TODO ubsłużyć przypadek >24
        print(f'Plik wczytany: {"{:.2f}".format(time.time() - current_time)}s')

    #MEASURE FUNCTION
    def measure_func_run_time_1000_times(self, func, name):
        current_time = time.time()
        for _ in range(1000):
            func()
        print(f'{name}: {"{:.2f}".format(time.time() - current_time)}s')

    #MEASURE DIJKSTRA
    def measure_simple_dijkstra(self):
        self.measure_func_run_time_1000_times(self.run_simple_dijkstra, 'simple dijkstra')

    def measure_medium_dijkstra(self):
        self.measure_func_run_time_1000_times(self.run_medium_dijkstra, 'medium dijkstra')

    def measure_long_dijkstra(self):
        self.measure_func_run_time_1000_times(self.run_long_dijkstra, 'long dijkstra')

    #MEASURE ASTAR
    def measure_simple_astar(self):
        self.measure_func_run_time_1000_times(self.run_simple_astar, 'simple astar')

    def measure_medium_astar(self):
        self.measure_func_run_time_1000_times(self.run_medium_astar, 'medium astar')

    def measure_long_astar(self):
        self.measure_func_run_time_1000_times(self.run_long_astar, 'long astar')

    #RUN DIJKSTRA
    def run_simple_dijkstra(self, print_result = False):
        dijkstra = Dijkstra(*self.simple_path, print_result)
        dijkstra.start_algorithm()

    def run_medium_dijkstra(self, print_result = False):
        dijkstra = Dijkstra(*self.medium_path, print_result)
        dijkstra.start_algorithm()

    def run_long_dijkstra(self, print_result = False):
        dijkstra = Dijkstra(*self.long_path, print_result)
        dijkstra.start_algorithm()

    #RUN ASTAR
    def run_simple_astar(self, print_result = False):
        astar = Astar(*self.simple_path, print_result)
        astar.start_algorithm()

    def run_medium_astar(self, print_result = False):
        astar = Astar(*self.medium_path, print_result)
        astar.start_algorithm()

    def run_long_astar(self, print_result = False):
        astar = Astar(*self.long_path, print_result)
        astar.start_algorithm()

if __name__=='__main__':#todo obsluzyc przypadek gdy przystanek nie istnieje/sciezka nie istnieje
    test = Test(FILE_PATH) 
    # test.measure_simple_dijkstra()
    # test.measure_simple_astar()
    test.run_long_astar(print_result=True)
