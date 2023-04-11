from copy import deepcopy

from MLGraph.multilayer_graph import *
from Tools.tools import *
from time import time


# from SuperNode import SuperNode


def get_triangle_connected_truss(graph: list[set[int]], query_nodes: list[int],
                                 truss_number_limit: int):
    """
    找到该层上包含查询顶点的密度最大的d-truss图
    :param graph: 邻接矩阵
    :param query_nodes: 查询顶点集合
    :param truss_number_limit: 最小的truss number限制
    :param remove_edges: 删除的边
    :return: 子图的邻接矩阵，边集合，顶点集合
    """

    subgraph = set()
    for node, neighbors in enumerate(graph):
        if len(neighbors) > 0:
            subgraph.add(node)
    delta = edge_decomposition(graph)
    truss_nodes = set()
    truss_edges = set()
    dsu = DSU(len(graph))
    for node, adjacency_list in enumerate(graph):
        for neighbor in adjacency_list:
            dsu.union(node, neighbor)

    root = dsu.find(query_nodes[0])
    for query_node in query_nodes:
        # 判断每个查询的顶点之间是否相邻
        if root != dsu.find(query_node):
            return truss_nodes
    edges = []
    for edge, number in delta.items():
        if number > truss_number_limit:
            edges.append(edge)
    visited = list()
    v_q = query_nodes[0]
    i = 0
    for u in graph[v_q].copy():
        edge = (min(u, v_q), max(u, v_q))
        if edge in edges and edge not in visited:
            need_visit = set(query_nodes.copy())
            need_visit.remove(v_q)
            if u in need_visit:
                need_visit.remove(u)
            truss_one = set()
            q = set()
            q.add(edge)
            visited.append(edge)
            # 找到所有和q相连的与这条边相关的最大truss
            while len(q) > 0:
                # i += 1
                edge = q.pop()
                x, y = edge
                truss_one.add(edge)
                for z in graph[x] & graph[y]:
                    i += 1
                    edge_s1 = (min(x, z), max(x, z))
                    edge_s2 = (min(y, z), max(y, z))
                    if edge_s1 in edges and edge_s2 in edges:
                        if z in need_visit:
                            need_visit.remove(z)
                        if edge_s1 not in visited:
                            graph[x].remove(z)
                            graph[z].remove(x)
                            q.add(edge_s1)
                            visited.append(edge_s1)
                        if edge_s2 not in visited:
                            graph[y].remove(z)
                            graph[z].remove(y)
                            q.add(edge_s2)
                            visited.append(edge_s2)
            if len(need_visit) == 0:
                truss_edges = truss_one
                break
    for u, v in truss_edges:
        if v > u:
            truss_nodes.add(u)
    truss_adjacency = [set() for _ in range(len(graph))]
    for u, v in truss_edges:
        truss_adjacency[u].add(v)
        truss_adjacency[v].add(u)
    return truss_adjacency, truss_nodes, truss_edges


def remove_edges_keep_truss_one_layer(graph: list[set[int]], edges: set[tuple], need_remove_edges: set[tuple[int, int]],
                                      k: int, remove_edges: set, edge_truss_number: dict[tuple, int], delete_edges):
    """
    在某一层上删除一些边，同时保证该层仍是truss 这里可以改为删除边的集合？
    :param delete_edges: 更改的边的truss number
    :param remove_edges: 删除的边
    :param graph: 单层图
    :param edges: 边的集合
    :param need_remove_edges: 需要删除的边
    :param k: 最小truss限制
    :param edge_truss_number: 该层每条边的truss number
    """
    Q_edge = set()
    for edge in need_remove_edges:
        Q_edge.add(edge)

    count = 0
    while len(Q_edge) > 0:
        count += 1
        edge = Q_edge.pop()
        x, y = edge
        graph[x].remove(y)
        graph[y].remove(x)
        edges.remove(edge)
        remove_edges.add(edge)
        for z in graph[x].copy() & graph[y].copy():
            edge_s1 = (min(x, z), max(x, z))
            edge_s2 = (min(y, z), max(y, z))
            # if edge_s1 not in edge_truss_number:
            #     print(layers, x, y, z)
            edge_truss_number[edge_s1] -= 1
            if edge_s1 not in delete_edges:
                delete_edges[edge_s1] = 0
            delete_edges[edge_s1] += 1
            edge_truss_number[edge_s2] -= 1
            if edge_s2 not in delete_edges:
                delete_edges[edge_s2] = 0
            delete_edges[edge_s2] += 1
            if edge_truss_number[edge_s1] < k:
                Q_edge.add(edge_s1)
            if edge_truss_number[edge_s2] < k:
                Q_edge.add(edge_s2)
    # print(count)


def add_edges_keep_truss_one_layer(graph: list[set[int]],
                                   edges: set[tuple], need_add_edges: set[tuple[int, int]], k: int):
    """
    将需要添加的边删除一些，保持邻接矩阵中所有的边都是truss
    :param graph: 单层图
    :param edges: 边的集合
    :param need_add_edges: 需要增加的边的集合
    :param k: 最小truss限制
    """
    flag = True
    while flag:
        flag = False
        for edge in need_add_edges.copy():
            u, v = edge
            triangle = len(graph[u] & graph[v])
            if triangle < k - 2:
                edges.remove(edge)
                need_add_edges.remove(edge)
                graph[u].remove(v)
                graph[v].remove(u)
                flag = True


def get_truss(graph: list[set[int]], edges: set[tuple], nodes: set[int], query_nodes: list[int], k, remove_edges=None,
              remove_nodes=None):
    """
    得到该层上包含查询顶点的truss
    :param remove_nodes: 这个过程中删除的顶点
    :param remove_edges: 这个过程中删除的边
    :param nodes: 顶点集合
    :param query_nodes: 查询顶点集合
    :param graph: 单层图
    :param edges: 边的集合
    :param k: 最小truss限制
    """
    if remove_nodes is None:
        remove_nodes = set()
    if remove_edges is None:
        remove_edges = set()
    Q_edge = set()
    edge_truss_number = edge_decomposition(graph)
    for edge in edges:
        if edge not in edge_truss_number.keys():
            Q_edge.add(edge)
    for edge, truss_number in edge_truss_number.items():
        if truss_number < k:
            Q_edge.add(edge)
    count = 0
    while len(Q_edge) > 0:
        count += 1
        edge = Q_edge.pop()
        x, y = edge
        graph[x].remove(y)
        graph[y].remove(x)
        edges.remove(edge)
        remove_edges.add(edge)
        for z in graph[x].copy() & graph[y].copy():
            edge_s1 = (min(x, z), max(x, z))
            edge_s2 = (min(y, z), max(y, z))
            edge_truss_number[edge_s1] -= 1
            edge_truss_number[edge_s2] -= 1
            if edge_truss_number[edge_s1] < k:
                Q_edge.add(edge_s1)
            if edge_truss_number[edge_s2] < k:
                Q_edge.add(edge_s2)
    print(count)
    # 保证其他顶点都与查询点连通
    dsu = DSU(len(graph))
    for edge in edges:
        u, v = edge
        dsu.union(u, v)
    root = dsu.find(query_nodes[0])

    for node in nodes.copy():
        if dsu.find(node) != root:
            nodes.remove(node)
            remove_nodes.add(node)
            for neighbor in graph[node]:
                if neighbor > node:
                    edges.remove((node, neighbor))
                    remove_edges.add((node, neighbor))
            graph[node] = set()
    for node in nodes.copy():
        # 如果该顶点的邻接矩阵是空的
        if not graph[node]:
            nodes.remove(node)
            remove_nodes.add(node)
