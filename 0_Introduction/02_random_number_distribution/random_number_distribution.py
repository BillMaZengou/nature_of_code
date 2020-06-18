import numpy as np
import matplotlib.pyplot as plt

random_count = np.zeros(100)
for i in range(1000):
    r = np.random.randint(0, 100)
    random_count[r] += 1

plt.bar(range(len(random_count)), random_count, width=1.0)
plt.show()
