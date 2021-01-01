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


def retreive_measurement():
    input_df = pd.read_csv('kf_data_validation.csv')
    # df_len = len(input_df)

    accX = np.array(input_df['AccX (m/s^2)'].tolist())      # converting into an array to \
    accY = np.array(input_df['AccY (m/s^2)'].tolist())      # iterate over each element \
    gyro = np.array(input_df['Gyro (deg/sec)'].tolist())    # to bring in form of measurement 'y'.

    z_theta = np.arctan2(-accY, accX)                       # y_theta = -ay/ax. output in radians
    z_dtheta = gyro * deg2rad                               # convert to rad/sec as input in deg/sec

    # for i in range(df_len):
    #     arr = np.array([y_theta[i], yw[i]])
    #     print(arr)
    return z_theta, z_dtheta