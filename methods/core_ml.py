import sys
import os
from time import time


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)


from DTruss.DTruss import *


def core_algorithm(graph: MultilayerGraph, core_number_limit: int, query_nodes: list[int]):
    graph_copy = deepcopy(graph)
    adjacency = graph_copy.adjacency_list
    degrees_layer_by_layer = graph.get_degrees_layer_by_layer()
    min_density = 100000
    layers_len = len(graph_copy.layers_iterator)
    layers = deepcopy(graph_copy.layers_iterator)
    for layer in graph_copy.layers_iterator:
        nodes = deepcopy(graph_copy.nodes_iterator)
        flag = True
        while flag:
            flag = False
            for node in nodes.copy():
                if degrees_layer_by_layer[layer][node] < core_number_limit:
                    flag = True
                    nodes.remove(node)
                    for neighbor in adjacency[layer][node]:
                        degrees_layer_by_layer[layer][neighbor] -= 1
                        adjacency[layer][neighbor].remove(node)
                    adjacency[layer][node] = set()
        edges = set()
        for node in nodes.copy():
            for neighbor in adjacency[layer][node]:
                if neighbor > node:
                    edges.add((node, neighbor))
        dsu = DSU(len(graph.nodes_iterator))
        for edge in edges:
            u, v = edge
            dsu.union(u, v)
        root = dsu.find(query_nodes[0])
        edges_len = len(edges)
        for node in nodes.copy():
            if dsu.find(node) != root:
                nodes.remove(node)
                edges_len -= len(adjacency[layer][node]) / 2
                adjacency[layer][node] = set()
        if edges_len == 0:
            layers_len -= 1
            layers.remove(layer)
            continue
        density = edges_len / len(nodes)
        if density < min_density:
            min_density = density
    print(min_density)
    print(layers)
    print(min_density * (layers_len ** 2))


if __name__ == '__main__':
    dataset = 'Yeast_2'
    ml_graph = MultilayerGraph(dataset)
    start = time()
    core_algorithm(ml_graph, 4, [5])
    end1 = time()
    print(end1 - start)
