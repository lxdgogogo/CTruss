import sys
import os
from time import time


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)

from MLGraph.multilayer_graph import MultilayerGraph
from methods.d_truss_baseline import baseline_algorithm
from methods.d_truss_connected import connected_algorithm
from methods.bottom_up import bottom_up_algorithm
from methods.top_down import top_down_algorithm
from methods.top_down_2 import top_down_algorithm_2

if __name__ == '__main__':
    # dataset = 'terrorist'
    # dataset = 'FAO'
    # dataset = 'test'
    # dataset = 'Yeast'
    # dataset = 'dblp'
    dataset = 'RM'
    ml_graph = MultilayerGraph(dataset)
    start = time()
    # print(baseline_algorithm(ml_graph, 5, 1, [5]))
    # baseline_algorithm(ml_graph, 5, 1, [5])
    # print(connected_algorithm(ml_graph, 5, 1, [5]))
    # bottom_up_algorithm(ml_graph, 5, 1, [5])
    # print(bottom_up_algorithm(ml_graph, 5, 1, [5]))
    top_down_algorithm(ml_graph, 5, 1, [5])
    # top_down_algorithm_2(ml_graph, 5, 5, [5])
    end1 = time()
    print(end1-start)


