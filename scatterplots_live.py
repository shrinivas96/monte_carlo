import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def generator():
    count = 0
    x = np.random.uniform(0, 1, 10)
    y = np.random.uniform(2, 3, 10)
    while count < 1000:
        count += 1
        x += 0.1
        y += 0.1    
        yield x, y


def animator(data, ax, scat):
    a, b = data
    # xmin, xmax = np.amin(a) - 0.2, np.amax(a) + 0.2
    # ymin, ymax = np.amin(b) - 0.2, np.amax(b) + 0.2

    # xmin, xmax = ax.get_xlim()
    # ymin, ymax = ax.get_xlim()

    # if np.amax(a) - xmax < 0.7:
    #     xmax += 0.7
    # if xmin - np.amin(a) < 0.7:
    #     xmin -= 0.7

    # if np.amax(b) - ymax < 0.7:
    #     ymax += 0.7
    # if ymin - np.amin(b) < 0.7:
    #     ymin -= 0.7

    # ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

    scat.set_offsets(np.c_[a, b])


def main():
    fig, ax = plt.subplots()
    ax.set(xlim=(-3, 6), ylim=(-3, 8))
    scat = ax.scatter(np.linspace(0, 1, 10), np.linspace(2, 3, 10), s=6)
    ani = FuncAnimation(fig=fig, 
                        func=animator, 
                        frames=generator, 
                        fargs=(ax, scat), 
                        interval=1000)

    plt.show()


if __name__ == '__main__':
    main()