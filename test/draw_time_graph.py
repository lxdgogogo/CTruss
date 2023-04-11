import matplotlib.pyplot as plt
import numpy as np
times = [0.028237935368491174, -0.007331770285904593, 1.8401945364578371, 1.794529064716107, 5.055933285255764,
         4.9882601438072065]
datasets = ['terrorist', 'RM', 'Yeast_2']
labels = datasets
width = 0.25
traditional = np.array(times[::2]) + 1
greedy = np.array(times[1::2]) + 1
x = np.arange(len(times)/2)
plt.bar(x - width / 2, traditional, width, label='traditional', fc='r')
plt.bar(x + width / 2, greedy, width, label='greedy', fc='b')
plt.xlabel('dataset')
plt.xticks(range(len(datasets)), labels=labels)
plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], labels=['0s', '0.01', '0.1s', '1s', '10s', '100s', '1000s', '10000s'])
plt.ylabel('Time')
plt.legend()
plt.savefig("time.png")
plt.show()
