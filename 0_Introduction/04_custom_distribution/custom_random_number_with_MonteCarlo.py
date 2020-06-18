import numpy as np
import matplotlib.pyplot as plt

def monteCarlo():
    selection = True
    while selection:
        r1 = np.random.rand()
        r2 = np.random.rand()

        probability = r1 * r1  # Custom function (only polynominal, for logrithmic r1 and r2 need modification)

        if r2 < probability:
            selection = False
    return r1

def main():
    random_count = np.zeros(100)
    for i in range(10000):
        r = int(monteCarlo() * 100)
        random_count[r] += 1

    plt.bar(range(len(random_count)), random_count, width=1.0)
    plt.show()

if __name__ == '__main__':
    main()
