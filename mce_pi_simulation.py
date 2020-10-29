"""
MC estimate of the value of pi based on the ratio of area of a circle of radius 'r' and
the area of a square of side '2r'.
We randomly place points in the range [-r, r] \times [-r, r], and count the particles
that fall inside the circle versus how many fall outside the circle.

Taken form the tutorial Monte Carlo Simulations: https://medium.com/towards-artificial-intelligence/monte-carlo-simulation-an-in-depth-tutorial-with-python-bcf6eb7856c8
"""
import math
import turtle
import random
import matplotlib.pyplot as plt


# visualise random points
myPen = turtle.Turtle()
myPen.hideturtle()
myPen.speed(0)

# draw the square
myPen.up()
myPen.setposition(-100, -100)
myPen.down()
myPen.fd(200)
myPen.left(90)
myPen.fd(200)

myPen.left(90)
myPen.fd(200)
myPen.left(90)
myPen.fd(200)
myPen.left(90)

# draw the circle
myPen.up()
myPen.setposition(0, -100)
myPen.down()
myPen.circle(100)


in_circle = 0
out_circle = 0

pi_list = []

plt.figure()
plt.axhline(y=math.pi, linestyle='dashed', label="True value")

for i in range(5):
    plot_list = []
    for j in range(1000):

        # randomly generate the numbers
        x = random.randrange(-100, 100)
        y = random.randrange(-100, 100)

        # check if they lie inside the circle
        if (x**2 + y**2 > 100**2):
            myPen.color("black")
            myPen.up()
            myPen.goto(x, y)
            myPen.down()
            myPen.dot()
            out_circle += 1

        else:
            myPen.color("red")
            myPen.up()
            myPen.goto(x, y)
            myPen.down()
            myPen.dot()
            in_circle += 1
        

        pi = 4 * in_circle / (in_circle + out_circle)

        pi_list.append(pi)
        plot_list.append(pi)

        avg_pi_errors = [abs(math.pi - pi) for pi in pi_list]
    label_txt = "Iteration " + str(i+1)
    plt.plot(plot_list, label=label_txt)
    print(pi_list[-1])

plt.title(r'MC estimate for value of $\pi$')
plt.xlabel("No. of iterations")
plt.ylabel("Estimated value")
plt.legend(loc="best")
plt.show()