"""
From Socratica YouTube tutorial on monte carlo and random walk:
The question is: What is the maximum number of walks you can take
so that the final distance from the start is 4 or less. If its more 
than 4 then you neeed a transport back home. 
"""

import random

def random_walk(steps):
    x, y = 0, 0
    for _ in range(steps):
        step = random.choice(['N', 'S', 'E', 'W'])
        if step == 'N':
            y += 1
        elif step == 'S':
            y -= 1
        elif step == 'E':
            x += 1
        else:
            x -= 1
    return (x, y)

def comp_random_walk(steps):
    """Return coordinates after 'steps' amount of random walks"""
    x, y = 0, 0
    for _ in range(steps):
        (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return x, y


def naive_RW():
    for _ in range(25):
        walk = comp_random_walk(10)
        print(walk, "Distance =", abs(walk[0]) + abs(walk[1]))


def main():
    number_of_walks = 30000
    for walk_length in range(1, 31):                                # Increase number of steps every time
        no_transport = 0                                            # Count the number of times we do not need a transport
        for _ in range(number_of_walks):                            # MC number_of_walks times simulation
            (x, y) = comp_random_walk(walk_length)                  # randomly walk walk_length steps
            distance = abs(x) + abs(y)                              # calculate distance from start point
            if distance <= 4:                               
                no_transport += 1                                   # increase counter if no transport needed
        no_trans_percent = float(no_transport) / number_of_walks    # percentage of time we did not need transport
        print("Walk size =", walk_length, 
              " and % of no transports =", no_trans_percent * 100)  # print it for each walk

if __name__ == "__main__":
    main()
