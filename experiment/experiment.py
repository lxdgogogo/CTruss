import sys
import os
from time import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)

from MLGraph.multilayer_graph import MultilayerGraph
from methods.top_down import top_down_algorithm

if __name__ == '__main__':
    # datasets = ['RM', 'Yeast_2', 'Yeast_2', 'dblp', 'terrorist']
    datasets = ['dblp']
    for dataset in datasets:
        print(dataset)
        ml_graph = MultilayerGraph(dataset)
        start = time()
        layer = int(len(ml_graph.layers_iterator) / 2)
        top_down_algorithm(ml_graph, 5, 2, [5])
        end1 = time()
        print("dataset : %s" % dataset)
        print("time : %s" % (end1 - start))
