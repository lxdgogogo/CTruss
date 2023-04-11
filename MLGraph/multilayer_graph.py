from array import array



class MultilayerGraph:
    def __init__(self, dataset_path=None):
        # ****** instance variables ******
        # layers
        self.number_of_layers = 0
        self.layers_iterator = set()
        self.layers_map = {}
        # nodes and adjacency list
        self.number_of_nodes = 0
        self.maximum_node = 0
        self.nodes_iterator = set()
        # 第一个索引是层，第二个索引是节点，第三个为该节点在该层上连接的边
        self.adjacency_list: list[list[set[int]]] = []
        self.edge_truss_number: list[dict[tuple, int]] = []
        # 每一层每一个边对应的truss number

        # if dataset_path has been specified
        if dataset_path is not None:
            # read the graph from the specified path
            self.load_dataset(dataset_path)
            # set the dataset path
            self.dataset_path = dataset_path

    def load_dataset(self, dataset_path):
        # open the file
        dataset_file_url = '../Datasets/' + dataset_path + '.txt'
        dataset_file = open(dataset_file_url)
        # read the first line of the file
        first_line = dataset_file.readline()
        split_first_line = first_line.split(' ')

        # set the number of layers
        self.number_of_layers = int(split_first_line[0])
        self.layers_iterator = set(range(self.number_of_layers))
        # set the number of nodes
        self.number_of_nodes = int(split_first_line[1])
        self.maximum_node = int(split_first_line[2])
        self.nodes_iterator = set(range(self.maximum_node + 1))
        # create the empty adjacency list
        self.adjacency_list: list[list[set]] = [[set() for _ in self.nodes_iterator] for _ in self.layers_iterator]
        # map and oracle of the layers
        layers_map = {}
        layers_oracle = 0

        # for each line of the file
        for _, line in enumerate(dataset_file):
            # split the line
            split_line = line.split(' ')
            layer = int(split_line[0])
            from_node = int(split_line[1])
            to_node = int(split_line[2])

            # if the layer is not in the map
            if layer not in layers_map:
                # add the mapping of the layer
                layers_map[layer] = layers_oracle
                self.layers_map[layers_oracle] = layer
                # increment the oracle
                layers_oracle += 1

            # add the undirected edge
            self.add_edge(from_node, to_node, layers_map[layer])
        self.edge_decomposition_layers()

    def add_edge(self, from_node, to_node, layer):
        # if the edge is not a self-loop
        if from_node != to_node:
            # add the edge
            self.adjacency_list[layer][from_node].add(to_node)
            self.adjacency_list[layer][to_node].add(from_node)

    # ****** nodes ******
    def get_nodes(self):
        if self.number_of_nodes == self.maximum_node:
            nodes = set(self.nodes_iterator)
            nodes.remove(0)
            return nodes
        else:
            return set(self.nodes_iterator)

    # ****** edges ******
    def get_number_of_edges(self, layer=None):
        number_of_edges = 0

        for neighbors in self.adjacency_list:
            for inner_layer, layer_neighbors in enumerate(neighbors):
                if layer is None:
                    number_of_edges += len(layer_neighbors)
                elif layer == inner_layer:
                    number_of_edges += len(layer_neighbors)

        return number_of_edges / 2

    def get_number_of_edges_layer_by_layer(self):
        number_of_edges_layer_by_layer = {}

        for layer in self.layers_iterator:
            number_of_edges_layer_by_layer[layer] = sum(
                [len(neighbors[layer]) for neighbors in self.adjacency_list]) / 2

        return number_of_edges_layer_by_layer

    # ****** layers ******
    def get_layer_mapping(self, layer):
        return self.layers_map[layer]

    def edge_decomposition_layers(self):
        """
        对truss进行分解
        :return: 一个列表 索引是第几层，内容是一个字典，edge:truss number,每条边只出现一次
        """
        edges_truss_number: list[dict[tuple, int]] = [{} for _ in self.layers_iterator]
        # edges = set()
        for layer in self.layers_iterator:
            edges_truss_number[layer] = edge_decomposition(self.adjacency_list[layer])
        #     edges.update(edges_truss_number[layer].keys())
        # for layer in self.layers_iterator:
        #     for edge in edges:
        #         if edge not in edges_truss_number[layer].keys():
        #             edges_truss_number[layer][edge] = 0
        self.edge_truss_number = edges_truss_number

    def remove_edge_one_layer(self, layer: int, edge: tuple):
        u, v = edge
        self.adjacency_list[layer][u].remove(v)
        self.adjacency_list[layer][v].remove(u)

    # def remove_edge(self, edge: tuple):
    #     """
    #     从图中删除一个边
    #     :param layer:第几层
    #     :param edge: 边
    #     """
    #     u, v = edge
    #     for layer in self.layers_iterator:
    #         self.adjacency_list[layer][u].remove(v)
    #         self.adjacency_list[layer][v].remove(u)
    #     self.keep_truss(edge)

    def remove_node(self, node: int):
        """
        从图中删除一个顶点
        :param node: 删除的顶点
        """
        for layer in self.layers_iterator:
            for neighbor in self.adjacency_list[layer][node]:
                self.remove_edge_one_layer(layer, (node, neighbor))

    def remove_edges_keep_truss(self, remove_edges_set: set[tuple], k: int, layers,
                                remove_edges: dict[tuple, list[int]],
                                delete_truss_number_edges: list[dict[tuple, int]]):
        Q_edge = remove_edges_set
        count = 0
        while len(Q_edge) > 0:
            count += 1
            edge = Q_edge.pop()
            x, y = edge
            # 在每一层上将该边删除
            for layer in layers:
                if y not in self.adjacency_list[layer][x]:
                    continue
                self.adjacency_list[layer][x].remove(y)
                self.adjacency_list[layer][y].remove(x)
                if edge not in remove_edges.keys():
                    remove_edges[edge] = []
                remove_edges[edge].append(layer)

                for z in self.adjacency_list[layer][x].copy() & self.adjacency_list[layer][y].copy():
                    edge_s1 = (min(x, z), max(x, z))
                    edge_s2 = (min(y, z), max(y, z))
                    self.edge_truss_number[layer][edge_s1] -= 1
                    self.edge_truss_number[layer][edge_s2] -= 1
                    if self.edge_truss_number[layer][edge_s1] < k:
                        Q_edge.add(edge_s1)
                    if self.edge_truss_number[layer][edge_s2] < k:
                        Q_edge.add(edge_s2)

                    if edge_s2 not in delete_truss_number_edges[layer].keys():
                        delete_truss_number_edges[layer][edge_s2] = 0
                    delete_truss_number_edges[layer][edge_s2] += 1
                    if edge_s1 not in delete_truss_number_edges[layer].keys():
                        delete_truss_number_edges[layer][edge_s1] = 0
                    delete_truss_number_edges[layer][edge_s1] += 1
        print(count)
    def recover_edges(self, remove_edges: dict[tuple, list[int]], delete_truss_number_edges: list[dict[tuple, int]]):
        for edge, layers in remove_edges.items():
            u, v = edge
            for layer in layers:
                self.adjacency_list[layer][v].add(u)
                self.adjacency_list[layer][u].add(v)
        for layer, edge_number in enumerate(delete_truss_number_edges):
            for edge, number in edge_number.items():
                self.edge_truss_number[layer][edge] += number

    def get_degrees_layer_by_layer(self):
        degrees_layer_by_layer: list[dict[int, int]] = [{}for _ in self.layers_iterator]
        for layer in self.layers_iterator:
            for node in self.nodes_iterator:
                degrees_layer_by_layer[layer][node] = len(self.adjacency_list[layer][node])
        return degrees_layer_by_layer


def edge_decomposition(graph: list[set[int]]):
    """
    对一层上的truss进行分解
    :return: 一个列表 索引是第几层，内容是一个字典，edge:truss number,每条边只出现一次
    """
    edges_truss_number: dict[tuple, int] = {}
    delta = compute_support(graph)
    sup_number_edges: dict[int, set] = {}
    for edge, sup_number in delta.items():
        if sup_number in sup_number_edges and sup_number != 0:
            sup_number_edges[sup_number].add(edge)
        elif sup_number != 0:
            sup_number_edges[sup_number] = set()
            sup_number_edges[sup_number].add(edge)
    # 计算每个边的truss number
    delta_layer = {}
    for edge, sup_numbers in delta.items():
        if sup_numbers != 0:
            delta_layer[edge] = sup_numbers
    # delta_layer = delta[:][layer]
    edges: set[tuple] = set(delta_layer.keys())
    if delta_layer:
        t_max = max(delta_layer.values())
    else:
        t_max = 0
    # 计算边的truss_number
    for t in range(1, t_max + 1):
        if len(edges) == 0:
            break
        if t not in sup_number_edges:
            continue
        needs = sup_number_edges[t]
        while len(needs) > 0:
            edge = needs.pop()
            edges.remove(edge)
            u, v = edge
            edges_truss_number[edge] = t + 2
            for neighbor in (graph[u] & graph[v] & edges):
                edge_s1 = (min(u, neighbor), max(u, neighbor))
                edge_s2 = (min(v, neighbor), max(v, neighbor))
                sup_number_edges[delta_layer[edge_s1]].remove(edge_s1)
                sup_number_edges[delta_layer[edge_s2]].remove(edge_s2)
                if (delta_layer[edge_s1] - 1) not in sup_number_edges:
                    sup_number_edges[delta_layer[edge_s1] - 1] = set()
                sup_number_edges[delta_layer[edge_s1] - 1].add(edge_s1)
                if (delta_layer[edge_s2] - 1) not in sup_number_edges:
                    sup_number_edges[delta_layer[edge_s2] - 1] = set()
                sup_number_edges[delta_layer[edge_s2] - 1].add(edge_s2)
                delta_layer[edge_s1] -= 1
                delta_layer[edge_s2] -= 1
                if delta_layer[edge_s1] == t - 1 and edge_s1 in edges:
                    needs.add(edge_s1)
                if delta_layer[edge_s2] == t - 1 and edge_s2 in edges:
                    needs.add(edge_s2)
    return edges_truss_number


def compute_support(graph: list[set[int]]):
    """
    对一个单层图计算各个边的support
    :param graph: 一层上边集合
    :param layers: 层的循环
    :param nodes: 子图包含的顶点列表
    :return: 返回值是dict,边到边的support值
    """
    # support of each edge in this layer
    delta = {}
    for node in range(len(graph)):
        for neighbor in graph[node]:
            if neighbor > node:
                delta[(node, neighbor)] = 0

    for node in range(len(graph)):
        for neighbor in graph[node]:
            if neighbor > node:
                common_neighbors = set(graph[node]) & set(graph[neighbor])
                for neighbor2 in common_neighbors:
                    if neighbor2 > neighbor:
                        delta[(node, neighbor)] += 1
                        delta[(node, neighbor2)] += 1
                        delta[(neighbor, neighbor2)] += 1
    return delta


# 计算子图中各个层上的边的数量
def compute_edges(multilayer_graph: list, layers: list, subgraph: set):
    """
    :param multilayer_graph: 多层图
    :param layers: 都有哪些层
    :param subgraph: 子图顶点集合
    :return: 子图中各个层都有多少边
    """
    layer_edge = {layer: 0 for layer in layers}
    for layer in layers:
        for node in subgraph:
            for neighbor in (multilayer_graph[layer][node] & subgraph):
                if neighbor > node:
                    layer_edge[layer] += 1
    return layer_edge


# 计算子图中各个层上的边的数量
def compute_edges_one_layer(graph: list[set], subgraph: set):
    """
    :param graph: 多层图
    :param subgraph: 子图顶点集合
    :return: 子图中各个层都有多少边
    """
    layer_edges = 0
    for node in subgraph:
        for neighbor in (graph[node] & subgraph):
            if neighbor > node:
                layer_edges += 1
    return layer_edges


def compute_density(multilayer_graph: list, layers: list, subgraph: set):
    """
    :param multilayer_graph: 多层图
    :param layers: 都有哪些层
    :param subgraph: 子图顶点集合
    :return: float类型 密度
    """
    if len(subgraph) == 0 or len(subgraph) == 1:
        return 0
    layer_number = len(layers)
    nodes_number = len(subgraph)
    layer_edge = compute_edges(multilayer_graph, layers, subgraph)
    edges = sum(layer_edge.values())
    density = (1 / layer_number) * 2 * edges / (nodes_number * (nodes_number - 1))
    return density


def compute_density_all(edges_len: int, node_len: int, layers_len: int, k=2):
    """
    :param layers_len: 层的多少
    :param k:
    :param edges_len: 边的数量
    :param node_len: 顶点的数量
    :return: float类型 密度
    """
    if node_len == 0 or edges_len == 0:
        return 0
    density = edges_len / node_len * (layers_len ** k)
    return density


def compute_internal_density(multilayer_graph: list, layers: list, subgraph: set):
    """
    :param multilayer_graph: 多层图
    :param layers: 都有哪些层
    :param subgraph: 子图顶点集合
    :return: float类型 密度
    """
    min_layer_edges = 0
    for layer in layers:
        layer_edges = compute_edges_one_layer(multilayer_graph[layer], subgraph)
        if layer_edges > min_layer_edges:
            min_layer_edges = layer_edges

    density = (len(layers) ** 2) * min_layer_edges / len(subgraph)
    return density


def compute_density_one_layer(edges: set[tuple]):
    """
    计算单层图上的密度
    :param edges: 边的集合
    :return: float类型 密度
    """

    if len(edges) == 0 or len(edges) == 1:
        return 0
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    nodes_number = len(nodes)
    density = 2 * len(edges) / (nodes_number * (nodes_number - 1))
    return density


def compute_internal_density_one_layer(edges: set[tuple]):
    """
    计算单层图上的平均度数
    :param edges: 边的集合
    :return: float类型 密度
    """

    if len(edges) == 0 or len(edges) == 1:
        return 0
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    density = len(edges) / len(nodes)
    return density
