from datastructures import *
from dijkstra import Dijkstra
from astar import Astar
import time
import random

FILE_PATH = './ignore/connection_graph.csv'

random.seed(16)#least not successful results

class Test:
    def __init__(self, file_path) -> None:
        current_time = time.time()
        self.graph = Graph(file_path)
        print(f'Plik wczytany: {"{:.2f}".format(time.time() - current_time)}s')
        self.nodes_len: int = len(self.graph.nodes.keys())
        self.stops: List[str] = [*self.graph.nodes.keys()]
        self.test_cases = []
        sample_size = 6
        for _ in range(sample_size):#hours <10:00
            self.test_cases.append((self.get_random_stop(), self.get_random_stop(), self.get_random_hour(3, 9)))
        for _ in range(sample_size):#hours 10:00-14:59
            self.test_cases.append((self.get_random_stop(), self.get_random_stop(), self.get_random_hour(10, 14)))
        for _ in range(sample_size):#hours 15:00-19:59
            self.test_cases.append((self.get_random_stop(), self.get_random_stop(), self.get_random_hour(15, 19)))
        for _ in range(sample_size):#hours >=20:00
            self.test_cases.append((self.get_random_stop(), self.get_random_stop(), self.get_random_hour(20, 29)))
            
        # for test_case in self.test_cases:
        #     print(test_case)


    def get_random_stop(self):
        return self.stops[random.randint(0, self.nodes_len - 1)]
    

    def get_random_hour(self, hourFrom, hourTo):
        return f'{random.randint(hourFrom,hourTo):02d}:{random.randint(0,59):02d}'

    #RUN ASTAR
    def run_dijkstra_random_tests(self):
        print('DIJKSTRA TESTS')
        astar = Dijkstra(self.graph)
        for test_case in self.test_cases:
            current_time = time.time()
            n = 10
            result = None
            for _ in range(n):
                result = astar.start_algorithm(*test_case, False)
            print(f'result {"   " if result else "not"} successful - {n} times - {test_case}: {"{:.2f}".format(time.time() - current_time)}s')
        print('===================================================================================')

    #RUN ASTAR
    def run_astar_random_tests(self):
        print('A* TESTS')
        astar = Astar(self.graph)
        for test_case in self.test_cases:
            current_time = time.time()
            n = 10
            result = None
            for _ in range(n):
                result = astar.start_algorithm(*test_case, False)#- cost: {result.cost if result else "  "} 
            print(f'result {"   " if result else "not"} successful - {n} times - {test_case}: {"{:.2f}".format(time.time() - current_time)}s')
        print('===================================================================================')


if __name__=='__main__':
    test = Test(FILE_PATH) 
    test.run_astar_random_tests()
    test.run_dijkstra_random_tests()
