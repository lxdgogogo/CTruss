from DTruss.DTruss import *


def connected_algorithm(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, query_nodes: list[int]):
    layer_set = get_subset(list(graph.layers_iterator), layer_limit)
    max_density = 0
    max_layer = set()
    max_nodes = set()
    max_adjacency = []
    for layers in layer_set:
        graph = copy.deepcopy(graph)
        # 先保证在这些层上的每条边的truss都大于等于k
        edge_truss_number: list[dict[tuple, int]] = graph.edge_truss_number
        edges = set()
        # 先得到所有层上的所有边
        for layer in graph.layers_iterator:
            for node in graph.nodes_iterator:
                for neighbor in graph.adjacency_list[layer][node]:
                    if neighbor > node:
                        edges.add((node, neighbor))
        # 先保证每一层上的每条边的truss number都大于等于t

        # 如果在某一层上边不构成三角形，则直接将该边删除即可
        remove_edges = {}
        for layer in layers:
            for edge in edges:
                if edge not in edge_truss_number[layer].keys():
                    graph.remove_edges_keep_truss(edge, truss_number_limit, layers, remove_edges)
        for layer in layers:
            edge_truss = edge_truss_number[layer]
            for edge, truss_number in edge_truss.items():
                # 如果该边没被访问过且truss number小于limit，则删除该边
                if truss_number < truss_number_limit and truss_number != -1:
                    graph.remove_edges_keep_truss(edge, truss_number_limit, layers, remove_edges)

        del edges
        edges = set()
        nodes = set()
        edge_adjacency = [set() for _ in graph.nodes_iterator]
        for node in graph.nodes_iterator:
            for neighbor in graph.adjacency_list[layers[0]][node]:
                if neighbor > node:
                    edges.add((node, neighbor))
                    nodes.add(node)
                    edge_adjacency[node].add(neighbor)

        dsu = DSU(len(graph.nodes_iterator))
        for edge in edges:
            u, v = edge
            dsu.union(u, v)
        root = dsu.find(query_nodes[0])
        for node in nodes.copy():
            if dsu.find(node) != root:
                nodes.remove(node)
                edge_adjacency[node] = set()

        if not set(query_nodes).issubset(nodes):
            continue

        truss_adjacency, truss_nodes, truss_edges =\
            get_triangle_connected_truss(edge_adjacency, query_nodes, truss_number_limit)
        if len(truss_nodes) == 0:
            continue
        density = (len(layers) ** 2) * len(truss_edges) / len(truss_nodes)
        if density > max_density:
            max_density = density
            max_layer = layers
            max_nodes = truss_nodes
            max_adjacency = truss_adjacency

        graph.recover_edges(remove_edges)
    return max_density, max_layer, max_nodes, max_adjacency



