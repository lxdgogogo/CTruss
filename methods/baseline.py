from CTruss.CTruss import *


def baseline_algorithm(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, query_nodes: list[int]):
    layer_set = get_subset(list(graph.layers_iterator), layer_limit)
    max_density = 0
    max_layer = set()
    max_nodes = set()
    max_adjacency: list[set[int]] = []
    max_edges = set()
    for layers in layer_set:
        if layers == [0, 1]:
            print(1)
        layer_0 = layers[0]
        edges = set()
        edge_adjacency: list[set] = [set() for _ in graph.nodes_iterator]
        for node in graph.nodes_iterator:
            for neighbor in graph.adjacency_list[layer_0][node]:
                if neighbor > node:
                    edges.add((node, neighbor))
        for edge in edges.copy():
            u, v = edge
            for layer_exist in layers:
                if v not in graph.adjacency_list[layer_exist][u]:
                    edges.remove(edge)
                    break
        for u, v in edges:
            edge_adjacency[u].add(v)
            edge_adjacency[v].add(u)
        # edge_truss_number = edge_decomposition(edge_adjacency)
        nodes = deepcopy(graph.nodes_iterator)
        get_truss(edge_adjacency, edges, nodes, query_nodes, truss_number_limit)
        if set(query_nodes).issubset(nodes):
            density = compute_density_all(len(edges), len(nodes), len(layers))
            if density > max_density:
                max_density = density
                max_layer = deepcopy(layers)
                max_nodes = deepcopy(nodes)
                max_adjacency = deepcopy(edge_adjacency)
                max_edges = deepcopy(edges)

    print(len(max_nodes))
    print(max_density)
    print(max_layer)
    print(len(max_edges))
    # truss = edge_decomposition(max_adjacency)
    return max_density, max_layer, max_nodes, max_adjacency