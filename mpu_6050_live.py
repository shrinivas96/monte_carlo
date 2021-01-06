from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from itertools import count
import pandas as pd
import random


plt.style.use('fivethirtyeight')
x_val = []
y_val = []

index = count()

def animate(i):
    data = pd.read_csv('data.csv')
    x = data["x_value"]
    y1 = data["total_1"]
    y2 = data["total_2"]


    # x_val.append(next(index))
    # y_val.append(random.randint(0, 5))

    plt.cla()
    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.tight_layout()
    plt.legend(loc="upper left")

live = FuncAnimation(plt.gcf(), animate, interval=1000)
# plt.plot(x_val, y_val)
plt.show()
