import matplotlib.pyplot as plt
import math
import numpy as np
densities = [81.23076923076923, 47.25, 963.4736842105264, 601.2432432432432, 31.94704684317719, 31]
datasets = ['terrorist', 'RM', 'Yeast_2']
labels = datasets
width = 0.25
traditional = np.log10(np.array(densities[::2]))
greedy = np.log10(np.array(densities[1::2]))
x = np.arange(len(densities) / 2)
plt.bar(x - width / 2, traditional, width, label='traditional', fc='r')
plt.bar(x + width / 2, greedy, width, label='greedy', fc='b')
plt.xlabel('dataset')
plt.xticks(range(len(datasets)), labels=labels)
plt.yticks([0, 1, 2, 3], labels=['0', '10', '100', '1000'])
plt.ylabel('Density')
plt.legend()
plt.savefig("density.png")
plt.show()
