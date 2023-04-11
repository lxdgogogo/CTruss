from DTruss.DTruss import *
from copy import deepcopy

global max_density
global max_layer
global max_nodes
global max_adjacency


def top_down_algorithm(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, query_nodes: list[int]):
    global max_density
    global max_layer
    global max_nodes
    global max_adjacency
    max_adjacency = []
    max_density = 0
    edges_dict = {}
    edges = set()
    adjacency = [set() for _ in graph.nodes_iterator]
    for layer in graph.layers_iterator:
        for node in graph.nodes_iterator:
            for neighbor in graph.adjacency_list[layer][node]:
                if neighbor > node:
                    edge = (node, neighbor)
                    if edge not in edges_dict.keys():
                        edges_dict[edge] = 0
                    edges_dict[edge] += 1

    nodes = deepcopy(graph.nodes_iterator)
    for edge, edge_number in edges_dict.items():
        if edge_number == graph.number_of_layers:
            u, v = edge
            edges.add(edge)
            adjacency[u].add(v)
            adjacency[v].add(u)
    get_truss(adjacency, edges, nodes, query_nodes, truss_number_limit)
    flag = len(edges) > 0
    top_down(graph, truss_number_limit, layer_limit, list(graph.layers_iterator), edges, adjacency,
             nodes, query_nodes, flag)
    edge_len = 0
    for node in graph.nodes_iterator:
        # if len(max_adjacency[node]) > 0:
        #     node_sum += 1
        edge_len += len(max_adjacency[node]) / 2
    print("max_density: %f" % max_density)
    print("edge_len: %f" % edge_len)
    print("max_layer: %s" % (str(max_layer)))
    print("max_nodes: %s" % (str(max_nodes)))
    # print(node_sum)
    return max_density, max_layer, max_nodes, max_adjacency


def top_down(graph: MultilayerGraph, truss_number_limit: int, layer_limit: int, layers: list, edges: set,
             adjacency: list[set], nodes: set[int], query_nodes: list[int], flag: bool):
    """
    自下而上遍历多层图
    :param graph: 多层图
    :param truss_number_limit: 最小truss限制
    :param layer_limit: 最小层数限制
    :param layers: 当前的层
    :param edges: 当前的边
    :param adjacency: 当前的邻接矩阵
    :param nodes: 当前的节点
    :param query_nodes: 查询顶点
    :param flag: 表示当前图是否和查询顶点连通
    :return: 返回最大密度，最大层数，最大子图，最大邻接矩阵
    """
    layer_max = graph.number_of_layers
    min_layer_delete = layer_max  # 当前层中最大的被删除的层
    min_layer_now = layer_max  # 当前层中最小的层
    for layer in layers:
        if min_layer_now > layer:
            min_layer_now = layer
    for layer in range(layer_max + 1):
        if layer not in layers:
            if min_layer_delete > layer:
                min_layer_delete = layer
    if len(layers) < layer_limit:
        return

    if set(query_nodes).issubset(nodes):
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

    if len(layers) == layer_limit:
        return


    for layer in range(min_layer_now, min_layer_delete):
        # print("layers%s remove layers %s" % (layers, layer))
        layers.remove(layer)
        # 对两层进行合并
        layers_num = len(layers)
        # 需要增加的边
        add_edges: set[tuple[int, int]] = set()
        # 需要删除的边
        remove_edges: set[tuple[int, int]] = set()
        # 需要增加的点
        add_nodes = set()
        # 需要删除的点
        remove_nodes = set()
        # 找到所有层都有，但是删除层上没有的边
        edges_dict = {}
        for layer_exist in layers:
            for node in graph.nodes_iterator:
                for neighbor in graph.adjacency_list[layer_exist][node]:
                    if neighbor > node and neighbor not in adjacency[node]:
                        edge = (node, neighbor)
                        if edge not in edges_dict.keys():
                            edges_dict[edge] = 0
                        edges_dict[edge] += 1
        for edge, edge_number in edges_dict.items():
            if edge_number == layers_num:
                add_edges.add(edge)
                edges.add(edge)
                u, v = edge
                if not adjacency[u]:
                    nodes.add(u)
                    add_nodes.add(u)
                if not adjacency[v]:
                    nodes.add(v)
                    add_nodes.add(v)
                adjacency[u].add(v)
                adjacency[v].add(u)
        # 如果不和查询顶点连通
        if not flag and set(query_nodes).issubset(nodes):
            # 如果当前的顶点中包含查询顶点，执行如下操作，不包含的话直接继续搜索就行
            # 如果是在该此循环时添加的查询顶点
            # 重新计算边，顶点，和邻接矩阵
            get_truss(adjacency, edges, nodes, query_nodes, truss_number_limit, remove_edges,
                      remove_nodes)
            if len(edges) == 0:
                for edge in remove_edges.copy():
                    u, v = edge
                    adjacency[u].add(v)
                    adjacency[v].add(u)
                    edges.add(edge)
                    remove_edges.remove(edge)
                for node in remove_nodes.copy():
                    nodes.add(node)
                    remove_nodes.remove(node)
            else:
                flag = True
        else:
            add_edges_keep_truss_one_layer(adjacency, edges, add_edges, truss_number_limit)
            # 合并
            dsu = DSU(len(graph.nodes_iterator) + 1)
            for edge in edges:
                u, v = edge
                dsu.union(u, v)
            root = dsu.find(query_nodes[0])
            for node in nodes.copy():
                if dsu.find(node) != root:
                    nodes.remove(node)
                    add_nodes.remove(node)
                    for neighbor in adjacency[node]:
                        if neighbor > node:
                            edges.remove((node, neighbor))
                            add_edges.remove((node, neighbor))
                    adjacency[node] = set()
        top_down(graph, truss_number_limit, layer_limit, layers, edges, adjacency, nodes,
                     query_nodes, flag)

        # 对图的邻接矩阵，顶点集合，边的集合和每层的truss number进行恢复
        for (u, v) in remove_edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
            edges.add((u, v))
        for node in remove_nodes:
            nodes.add(node)
        for (u, v) in add_edges:
            adjacency[u].remove(v)
            adjacency[v].remove(u)
            edges.remove((u, v))
        for node in add_nodes:
            nodes.remove(node)

        layers.append(layer)
