"""
A demo for plotting live data. Currenlty only plots data from a csv.
Next step is to plot data from a live IMU or some sensor.

Inspiration from this stack exhcange answer: https://stackoverflow.com/a/29834816/6609148

Also given in this offcial Matplotlib example: https://matplotlib.org/examples/animation/animate_decay.html
"""


import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('tkagg') 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Global contants needed throughout
deg2rad = np.pi / 180                                   # multiply to convert to radians
rad2deg = 180 / np.pi                                   # multiply to convert to degrees
T = 0.01                                                # sampling time. new measuements at every T seconds
I = np.identity(3)                                      # identity matrix
zero_mean = np.array([0.0, 0.0, 0.0])                   # to construct any N(0, Cov) and draw samples from it 
# np.random.seed(0)                                       # ensures we get the same random results each time


def csv_generator(flag):
    """
    Generator function to yield a new theta and dtheta value at each iteration.
    Needed by the animation function to get a new value at each 'interval' seconds.
    
    
    Parameters:
    flag: to return the measurements (0) or the true data (1). 

    Yeilds a zip of:
    z_theta: tangent funtion of accelerometer data. unit in radians
    z_dtheta: the gyroscope measurements converted to radian/sec

    theta_true: true value of the tilt angle. unit in radians
    dtheta_true: true value of the angular velocity. unit in radians/sec
    """
    input_df = pd.read_csv('kf_data_validation.csv')

    if flag == 0:
        accX = np.array(input_df['AccX (m/s^2)'].tolist())      # converting into an array to \
        accY = np.array(input_df['AccY (m/s^2)'].tolist())      # iterate over each element \
        gyro = np.array(input_df['Gyro (deg/sec)'].tolist())    # to bring in form of measurement 'y'.
        
        z_theta = np.arctan2(-accY, accX)                       # y_theta = -ay/ax. output in radians
        z_dtheta = gyro * deg2rad                               # convert to rad/sec as input in deg/sec

        for z_t, z_dt in zip(z_theta, z_dtheta):
            yield z_t, z_dt

    elif flag == 1:
        theta_true = np.array(input_df['Theta (deg)'].tolist())         # true value of theta to compare with estimated
        dtheta_true = np.array(input_df['Gyro45(deg/sec)'].tolist())    # true value of dtheta to compare with estimated
        
        theta_true = theta_true * deg2rad                   # converting the unit to randians
        dtheta_true = dtheta_true * deg2rad                 # converting the unit to randians/sec

        for th, dth in zip(theta_true, dtheta_true):
            yield th, dth

    else:
        raise ValueError("Value should either be 0 or 1.")


def animator(data, lines, axes):
    """
    Animator function to run for each frame in FuncAnimation after every 'interval' seconds.

    Parameters:
    data: Return from the generator that yeilds an array of theta and dtheta
    lines: Array of Line2D objects to set the new data to.
    axes: Array of axes generated from the subplots. To change the limits of axes when needed.

    Returns:
    lines: Modified array of Line2D objects after setting new data to it. Required by FuncAnimation for blit == True
    """

    theta_t, dtheta_t = data                    # generator returns a tuple of theta and dtheta.
                                                # this is the new data that needs to be plotted

    # We get all three axes' data and then append new data to it.
    xdata = lines[0].get_data()[0]              # essentially range(len(theta_t))
    yth_data = lines[0].get_data()[1]           # extract previous data that has already been plotted
    ydth_data = lines[1].get_data()[1]          # extract previous data that has already been plotted

    xdata = np.append(xdata, len(xdata) + 1)    # appends the next number to the list to create range(len(theta_t))
    yth_data = np.append(yth_data, theta_t)     # appends theta and dtheta for both the axes \
    ydth_data = np.append(ydth_data, dtheta_t)  # to the existing data.
    

    for ax in axes:                             # to check if data has reached max range of limits on both axes
        xmin, xmax = ax.get_xlim() 
        ymin, ymax = ax.get_ylim()
        if xdata[-1] >= xmax:
            ax.set_xlim(xmin, 3*xmax)
            ax.figure.canvas.draw()

        if (np.amin(yth_data) <= ymin) or (np.amin(ydth_data) <= ymin):
            ax.set_ylim(-1.7*ymin, ymax)
            ax.figure.canvas.draw()
        
        if (np.amax(yth_data) >= ymax) or (np.amax(ydth_data) >= ymax):
            ax.set_ylim(ymin, ymax*2)
            ax.figure.canvas.draw()


    lines[0].set_data(xdata, yth_data)          # finally set the new data to both the axes
    lines[1].set_data(xdata, ydth_data)

    return lines



def main():
    fig, axes = plt.subplots(2, 1)

    for ax in axes:
        ax.set_xlabel("Number of Measurements")
    axes[0].set_ylabel(r"Tilt Angle $\theta$ ($rad$)")
    axes[1].set_ylabel(r"Angular Velocity $\dot\theta$ ($rad/sec$)")


    line1, = axes[0].plot([], [], lw=2, color='b')      # return Line2D objects to change later. comma after \
    line2, = axes[1].plot([], [], lw=2, color='r')      # objects because axes.plot could return multiple items
    lines = np.array([line1, line2])

    fig.suptitle(r"Live PLot of $\theta$ and $\dot\theta$", fontsize=20)
    
    ani = FuncAnimation(fig=fig,                        # pass the figure to animate
                        func=animator,                  # function to update the figure each frame
                        frames=csv_generator(0),        # argument for function. generator object
                        fargs=(lines, axes,),           # additional arguments. should always be a tuple
                        blit=True,                      # copies pixels from the last frame for fast rendering
                        interval=10)                    # update frequency

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

