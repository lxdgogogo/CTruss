from DTruss.DTruss import *


def baseline_algorithm(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, query_nodes: list[int]):
    layer_set = get_subset(list(graph.layers_iterator), layer_limit)
    max_density = 0
    max_layer = set()
    max_nodes = set()
    max_adjacency: list[set] = []
    graph_adjacency_copy = deepcopy(graph.adjacency_list)
    edge_truss_number_copy = deepcopy(graph.edge_truss_number)
    for layers in layer_set:
        # if layers == [0, 1, 3, 4, 5]:
        #     print(1)
        # 先保证在这些层上的每条边的truss都大于等于k
        edge_truss_number: list[dict[tuple, int]] = graph.edge_truss_number
        # edge_truss_number: list[dict[tuple, int]] = deepcopy(graph.edge_truss_number)
        delete_truss_number_edges = [{} for _ in graph.layers_iterator]
        edges = set()
        # 先得到所有层上的所有边
        for layer in graph.layers_iterator:
            for node in graph.nodes_iterator:
                for neighbor in graph.adjacency_list[layer][node]:
                    if neighbor > node:
                        edges.add((node, neighbor))
        # 先保证每一层上的每条边的truss number都大于等于t
        # 如果在某一层上边不构成三角形，则直接将该边删除即可
        remove_edges_set = set()
        remove_edges: dict[tuple, list[int]] = {}
        for layer in layers:
            for edge in edges:
                if edge not in edge_truss_number[layer].keys():
                    remove_edges_set.add(edge)
        for layer in layers:
            edge_truss = edge_truss_number[layer]
            for edge, truss_number in edge_truss.items():
                if truss_number < truss_number_limit:
                    remove_edges_set.add(edge)

        graph.remove_edges_keep_truss(remove_edges_set, truss_number_limit, layers, remove_edges,
                                      delete_truss_number_edges)
        # 如果该边没被访问过且truss number小于limit，则删除该边

        del edges
        edges = set()
        nodes = set()
        edge_adjacency = [set() for _ in graph.nodes_iterator]
        for node in graph.nodes_iterator:
            for neighbor in graph.adjacency_list[layers[0]][node]:
                edges.add((node, neighbor))
                nodes.add(node)
                nodes.add(neighbor)
                edge_adjacency[node].add(neighbor)

        dsu = DSU(len(graph.nodes_iterator))
        for edge in edges:
            u, v = edge
            dsu.union(u, v)
        root = dsu.find(query_nodes[0])
        edges_len = len(edges)/2
        for node in nodes.copy():
            if dsu.find(node) != root:
                nodes.remove(node)
                edges_len -= len(edge_adjacency[node])/2
                edge_adjacency[node] = set()

        if set(query_nodes).issubset(nodes):
            density = compute_density_all(int(edges_len), len(nodes), len(layers))
            if density > max_density:
                max_density = density
                max_layer = deepcopy(layers)
                max_nodes = deepcopy(nodes)
                max_adjacency = deepcopy(edge_adjacency)
        graph.recover_edges(remove_edges, delete_truss_number_edges)
        # print()
    # print(max_adjacency)
    edge_len = 0
    for node in max_nodes:
        edge_len += len(max_adjacency[node]) / 2
    print(len(max_nodes))
    print(edge_len)
    print(max_density)
    print(max_layer)
    print(graph.adjacency_list == graph_adjacency_copy)
    print(edge_truss_number_copy == graph.edge_truss_number)
    return max_density, max_layer, max_nodes, max_adjacency


# 通过层的dfs搜索，得到
