class SuperNode:
    def __init__(self, truss_number):
        self.edges: list[tuple] = []
        self.truss_number = truss_number
        self.children: list[SuperNode] = []

    def add_edge(self, edge: tuple):
        self.edges.append(edge)

    def add_children(self, super_node):
        self.children.append(super_node)


def find_edges(edge: tuple, root: SuperNode):
    if edge in root.edges:
        return root
    elif len(root.children) == 0:
        return None
    else:
        for node in root.children:
            edge_node = find_edges(edge, node)
            if edge_node is not None:
                return edge_node
