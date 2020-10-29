"""
Monte Carlo Estimate of integral of sin x in the limits [0, pi] using a Uniform random variable.
Taken and changed from a tutorial Monte Carlo Integration by Andrew Doston: https://youtu.be/WAf0rqwAvgg


The monte carlo estimate of the integral is given by:
\int_b^a \approx (b-a) * \sum_i f(x_i) \frac{1}{N}.
"""
# from scipy import random
import numpy as np
import matplotlib.pyplot as plt


def sinx(x):
    return np.sin(x)


def main():
    int_a, int_b = 0.0, np.pi                           # limits of integration
    N = 10000                                           # how many samples?

    xrand = np.random.uniform(int_a, int_b, N)          # randomly draw samples x_i's from a Uniform distibution N times
    y_x = sinx(xrand)                                   # f(x_i)'s
    summation = np.sum(y_x)                             # sum of all f(x_i)'s
    integral = (int_b * summation) / float(N)

    print("Integral of sin(x) in the limits [0, pi] = ", integral)


def longer_main():
    # the longer way of doing the same stuff as main() for plotting purposes:

    int_a, int_b = 0.0, np.pi                           # limits of integration
    N = 10000                                           # how many samples?

    xrand = np.random.uniform(int_a, int_b, N)          # randomly draw samples x_i's from a Uniform distibution N times

    summation = 0.0                                     # sum of all f(x_i)'s
    y_x = []                                            # y = f(x_)
    integrals = []                                      # save value of approx area after each iteration
    for count, xs in enumerate(xrand):
        f_x = sinx(xs)              # find f(x)
        y_x.append(f_x)             # add that to list y
        summation += f_x            # find sum of f(x)'s

        integral = (int_b * summation) / float(count+1) 
        integrals.append(integral)

    plt.figure()
    plt.axhline(y=2.0, color='g', linestyle='dashed', label="True value")
    plt.plot(integrals, label='MC estimate')            # the plot shows gradual convergence to the true value
    plt.title(r'MC estimate of area under $\int_0^{\pi} sin(x)$')
    plt.xlabel("No. of iterations")
    plt.ylabel("Estimated area")
    plt.legend(loc="best")
    plt.show()


def repeated_main():
    int_a, int_b = 0.0, np.pi                           # limits of integration
    N = 10000                                           # how many samples?
    M = 1000                                            # how many iterations?
    areas = []                                          # save approximation of all M iterations

    for _ in range(M):
        xrand = np.random.uniform(int_a, int_b, N)      # randomly draw samples x_i's from a Uniform distibution N times
        y_x = sinx(xrand)

        summation = np.sum(y_x)                         # sum of all f(x_i)'s
        integral = (int_b * summation) / float(N)

        areas.append(integral)
    
    plt.figure()
    plt.title("Distribution of areas calculated")
    plt.hist(areas, bins=30, ec='black')
    plt.xlabel("Estimated areas")
    ytext = "No of times out of " + str(M)
    plt.ylabel(ytext)
    plt.show()


if __name__ == "__main__":
    longer_main()