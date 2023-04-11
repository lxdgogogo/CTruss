import itertools


def get_subset(items: list, number: int):
    """
    :param items: 原始列表
    :param number: 产生的子集的最小长度
    :return: 所有产生的子集
    """
    n = len(items)
    result = []
    for i in range(2 ** n):  # 子集的个数
        combo = []
        for j in range(n):  # 用来判断二进制数的下标为j的位置的数是否为1
            if (i >> j) % 2:  # 模2判断二进制的最后一个数是否为1
                combo.append(items[j])
        if len(combo) >= number:
            result.append(combo)
    return result


# disjoint set union
class DSU:
    def __init__(self, num: int):
        self.root = [i for i in range(num)]

    def find(self, k):
        if k >= len(self.root):
            print(k)
        if self.root[k] == k:
            return k
        self.root[k] = self.find(self.root[k])
        return self.root[k]

    def union(self, a, b):
        x = self.find(a)
        y = self.find(b)
        if x != y:
            self.root[y] = x
        return


class cartesian(object):
    def __init__(self):
        self._data_list: list[list[set[int]]] = []

    def add_data(self, data: list[set[int]] = None):  # 添加生成笛卡尔积的数据列表
        if data is None:
            data = []
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        items = []
        for item in itertools.product(*self._data_list):
            items.append(item)
        return items
