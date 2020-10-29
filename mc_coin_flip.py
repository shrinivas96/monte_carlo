"""
Simulating a simple coin flip. Could not find the source of this code.
"""

import random
import numpy as np 
import matplotlib.pyplot as plt

def coin_flip():
    """Simulate flipping of a coin where 0 is Heads and 1 is Tails"""
    return random.randint(0, 1)

prob_list = []
def monte_carlo(n):
    results = 0
    for i in range(n):
        flip_result = coin_flip()               # perform the flip
        results += flip_result                  # add the result to the sum 

        probability = results/(i+1)             # calculate current probability after each flip 
        prob_list.append(probability)           # list of change of probability after each flip

        plt.axhline(y=0.5, color='r', linestyle='-')
        plt.xlabel("Iterations")
        plt.ylabel("Probability")
        plt.plot(prob_list)

    return results/n

flip5k = monte_carlo(5000)
print(flip5k)