from DTruss.DTruss import *
from copy import deepcopy

global max_density
global max_layer
global max_nodes
global max_adjacency


def bottom_up_algorithm(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, query_nodes: list[int]):
    global max_density
    global max_layer
    global max_nodes
    global max_adjacency
    max_density = 0
    nodes = deepcopy(graph.nodes_iterator)
    edge_truss_number = {}
    edges = set()
    adjacency = [set() for _ in nodes]
    for layer in graph.layers_iterator:
        for node in nodes:
            for neighbor in graph.adjacency_list[layer][node]:
                adjacency[node].add(neighbor)
                if neighbor > node:
                    edges.add((node, neighbor))

    edge_truss_number = edge_decomposition(adjacency)
    bottom_up(graph, truss_number_limit, layer_limit, [], edges, adjacency,
              nodes, edge_truss_number, query_nodes)
    edge_len = 0
    for node in max_nodes:
        edge_len += len(max_adjacency[node]) / 2
    print("max_density: %f" % max_density)
    print("edge_len: %f" % edge_len)
    print("max_layer: %s" % (str(max_layer)))
    print("max_nodes: %s" % (str(max_nodes)))
    return max_density, max_layer, max_nodes, max_adjacency


def bottom_up(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, layers: list, edges: set,
              adjacency: list[set], nodes: set[int], edge_truss_number: dict[tuple, int], query_nodes: list[int]):
    """
    自下而上遍历多层图
    :param graph: 多层图
    :param truss_number_limit: 最小truss限制
    :param layer_limit: 最小层数限制
    :param layers: 当前的层
    :param edges: 当前的边
    :param adjacency: 当前的邻接矩阵
    :param nodes: 当前的节点
    :param edge_truss_number: 当前层每条边对应的truss number
    :param query_nodes: 查询顶点
    :return: 返回最大密度，最大层数，最大子图，最大邻接矩阵
    """
    # 当前遍历的最大层
    if len(layers) == 0:
        max_layer_now = 0
    else:
        max_layer_now = max(layers) + 1
    layer_max = graph.number_of_layers
    if len(layers) >= layer_limit:
        density = compute_density_all(len(edges), len(nodes), len(layers))
        global max_density
        global max_layer
        global max_nodes
        global max_adjacency
        if density > max_density:
            max_density = density
            max_layer = deepcopy(layers)
            max_nodes = deepcopy(nodes)
            max_adjacency = deepcopy(adjacency)
    if max_layer_now > max(graph.layers_iterator):
        return

    for layer in range(max_layer_now, layer_max):
        adjacency_layer = graph.adjacency_list[layer]
        # print("layers%s to layers %s" % (layers, layer))
        layers.append(layer)
        layer_truss_number: dict = graph.edge_truss_number[layer]
        # 对两层进行合并
        # 需要删除的边
        need_remove_edges: set[tuple[int, int]] = set()
        # 需要删除的点
        need_remove_nodes = set()
        # 已经删除的边
        remove_edges: set[tuple[int, int]] = set()
        delete_truss_number_edges = {}
        # 如果扩展层没有该边或者该边的truss number小于k，则直接将该边删除即可
        for node in nodes:
            for neighbor in adjacency[node]:
                if neighbor > node:
                    edge = (node, neighbor)
                    # 如果扩展层没有该边或者该边不构成三角形
                    # if neighbor not in adjacency_layer[node] or not layer_truss_number.__contains__(edge):
                    #     need_remove_edges.add(edge)
                    #     continue
                    # if layer_truss_number[edge] < truss_number_limit:
                    #     need_remove_edges.add(edge)
                    if neighbor not in adjacency_layer[node]:
                        need_remove_edges.add(edge)
        # print("len need: %d" % len(need_remove_edges))
        # for edge in need_remove_edges:
        remove_edges_keep_truss_one_layer(adjacency, edges, need_remove_edges, truss_number_limit,
                                          remove_edges, edge_truss_number, delete_truss_number_edges)
        for node in nodes:
            if not adjacency[node]:
                need_remove_nodes.add(node)

        remove_nodes: set[int] = set()
        dsu = DSU(len(graph.nodes_iterator) + 1)
        for edge in edges:
            u, v = edge
            dsu.union(u, v)
        root = dsu.find(query_nodes[0])
        for node in nodes.copy():
            if dsu.find(node) != root:
                nodes.remove(node)
                for neighbor in adjacency[node]:
                    if neighbor > node:
                        edges.remove((node, neighbor))
                        remove_edges.add((node, neighbor))
                adjacency[node] = set()
                remove_nodes.add(node)

        if set(query_nodes).issubset(nodes):
            bottom_up(graph, truss_number_limit, layer_limit, layers, edges, adjacency, nodes,
                      edge_truss_number, query_nodes)

        # 对图的邻接矩阵，顶点集合，边的集合和每层的truss number进行恢复
        for (u, v) in remove_edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
            edges.add((u, v))
        for node in remove_nodes:
            nodes.add(node)
        for edge, delete_number in delete_truss_number_edges.items():
            edge_truss_number[edge] += delete_number
        layers.remove(layer)
