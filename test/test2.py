def fun(layers: set[int], nums):
    max_layer_now = nums  # 当前层中最小的被删除的层
    min_layer_now = nums  # 当前层中最小的层
    for layer in layers:
        if min_layer_now > layer:
            min_layer_now = layer
    for layer in range(1, nums + 1):
        if layer not in layers:
            if max_layer_now > layer:
                max_layer_now = layer
    print(min_layer_now)
    print(max_layer_now)


# a = set()
# a.update([1, 3, 4])
# fun(a, 5)

c1 = set()
c1.add(1)
c2 = set()
c2.add(1)
a = list[c1]
b = list[c2]
print(a == b)

d1 = [1, 2]
d2 = [2, 1]
print(d1 == d2)