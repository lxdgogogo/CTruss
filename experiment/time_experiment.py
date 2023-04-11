from MLGraph.multilayer_graph import MultilayerGraph
from methods.d_truss_baseline import baseline_algorithm
from methods.d_truss_connected import greedy_algorithm
import matplotlib.pyplot as plt
from time import time
import math


if __name__ == '__main__':
    datasets = ['terrorist', 'RM']
    labels = datasets
    width = 0.25
    times = []
    for x in range(len(datasets)):
        dataset = datasets[x]
        ml_graph = MultilayerGraph(dataset)
        # print(ml_graph.edge_decomposition_layers())
        start = time()
        print(greedy_algorithm(ml_graph, 3, 1, [5]))
        end = time()
        t1 = math.log10(end - start)
        ml_graph2 = MultilayerGraph(dataset)
        start2 = time()
        print(baseline_algorithm(ml_graph2, 3, 1, [5]))
        end2 = time()
        t2 = math.log10(end2 - start2)
        times.append(t1)
        times.append(t2)
        plt.bar(x - width / 2, t1, width, label='traditional', fc='r')
        plt.bar(x + width / 2, t2, width, label='greedy', fc='b')
        # plt.show()
    print(times)
    plt.xticks(range(len(datasets)), labels=labels)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], labels=['0s', '0.01', '0.1s', '1s', '10s', '100s', '1000s', '10000s'])
    plt.ylabel('Time')
    plt.legend()
    plt.show()

