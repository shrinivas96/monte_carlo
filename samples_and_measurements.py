import numpy as np
import pandas as pd

# Global contants for converting units
deg2rad = np.pi / 180
rad2deg = 180 / np.pi

def uniform_samples(a = -1, b = 1, n = 100, d = 2):
    """
    Returns n d-dimensional samples that are uniformly distributed in the half \
    open interval [a, b)
    """
    samples = (b - a) * np.random.random((n, d)) + a
    return samples


def retreive_data(flag = 0):
    """
    Function to return measured data and ground truth values from a csv
    The header of the csv looks like this:
    Time (sec), Voltage (V), AccX (m/s^2), AccY (m/s^2), Gyro (deg/sec), Gyro45(deg/sec), Theta (deg)
    
    This csv can be used to validate your filter model.


    The last two columns are true values recorded with an encoder and unbiased gyroscope.

    Parameters:
    flag: what to return: measurement data(0) or ground truth(1)

    Returns:
    z_theta and z_dtheta if flag = 0
    theta_true, dtheta_true if flag = 1


    z_theta: tangent funtion of accelerometer data. unit in radians
    z_dtheta: the gyroscope measurements converted to radian/sec

    theta_true: true value of the tilt angle. unit in radians
    dtheta_true: true value of the angular velocity. unit in radians/sec
    """
    input_df = pd.read_csv('kf_data_validation.csv')
    # df_len = len(input_df)

    if flag == 0:
        accX = np.array(input_df['AccX (m/s^2)'].tolist())      # converting into an array to \
        accY = np.array(input_df['AccY (m/s^2)'].tolist())      # iterate over each element \
        gyro = np.array(input_df['Gyro (deg/sec)'].tolist())    # to bring in form of measurement 'y'.
        
        z_theta = np.arctan2(-accY, accX)                       # y_theta = -ay/ax. output in radians
        z_dtheta = gyro * deg2rad                               # convert to rad/sec as input in deg/sec

        return z_theta, z_dtheta

    elif flag == 1:
        theta_true = np.array(input_df['Theta (deg)'].tolist())         # true value of theta to compare with estimated
        dtheta_true = np.array(input_df['Gyro45(deg/sec)'].tolist())    # true value of dtheta to compare with estimated
        
        theta_true = theta_true * deg2rad                   # converting the unit to randians
        dtheta_true = dtheta_true * deg2rad                 # converting the unit to randians/sec

        return theta_true, dtheta_true
    
    else:
        raise ValueError("Value should either be 0 or 1.")