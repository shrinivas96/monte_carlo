import numpy as np
import pandas as pd
import scipy
import scipy.stats as st
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
# from mpl_toolkits.mplot3d import Axes3D

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


def state_likelihood(z_t, mean, cov):
    """
    Returns the multivariate gaussian likelihood of z_t given x_t.
    Parameters:
    z_t: 2x1 vector of the observed measurement
    mean: 2x1 vector of expected measurement, mean = C x_t
    cov: 2x2 measurement noise matrix (pos-semi-def)
    
    L(z_t) = (2 pi)^(-k/2) * |cov|^(-1/2) * e ^ {-0.5 * (z - mu)^T . cov^(-1) . (z - mu)}
    """
    k = z_t.size                                    # dimension of the vector 
    e1 = (2 * np.pi) ** (-k/2)                      # first expression of likelihood

    cov_sqrt_det = np.linalg.det(cov) ** (-1/2)     # square root of the determinant of covariance matrix
    cov_inverse = np.linalg.inv(cov)                # inverse of the covariance matrix

    z_mean_diff = (z_t - mean)                                                  # difference between observed and expected measurement
    z_mean_diff_T = (z_t - mean).T                                              # transpose of above
    exponential = np.exp(-0.5 * (z_mean_diff_T @ cov_inverse @ z_mean_diff))    # exponential part of the likelihood function

    likelihood = e1 * cov_sqrt_det * exponential                                # the likelihood L(z_t)
    return likelihood


def retreive_measurement():
    input_df = pd.read_csv('kf_data_validation.csv')
    df_len = len(input_df)

    accX = np.array(input_df['AccX (m/s^2)'].tolist())      # converting into an array to \
    accY = np.array(input_df['AccY (m/s^2)'].tolist())      # iterate over each element \
    gyro = np.array(input_df['Gyro (deg/sec)'].tolist())    # to bring in form of measurement 'y'.

    z_theta = np.arctan2(-accY, accX)                       # y_theta = -ay/ax. output in radians
    z_dtheta = gyro * deg2rad                               # convert to rad/sec as input in deg/sec

    # for i in range(df_len):
    #     arr = np.array([y_theta[i], yw[i]])
    #     print(arr)
    return z_theta, z_dtheta


def main():
    """
    Generates uniform samples to span the space of the states, 
    and propagates through one iteration of the particle filter
    algorithm without the resampling step.
    """

    T = 0.01                            # sampling time. new measuements at every T seconds
    a, b = -0.5, 0.5                    # interval to generate uniform particles
    n_samples = 100                     # number of samples
    dim = 3                             # vector dimension for 3 states to be estimated
    np.random.seed(0)
    
    qw = 5                              # uncertainty in w
    qb = 0.01                           # uncertainty in b
    q_01 = (T ** 2) * qw / 2
    Qd = np.array([[T * qw, q_01, 0],                       # motion covariance
                   [q_01, (T ** 3) * qw / 3, 0], 
                   [0, 0, T * qb]])


    # Actual measurements taken from the csv
    z_theta, z_dtheta = retreive_measurement()              # unit rad, rad/sec
    rw = 10 ** (-6)
    r_theta = 5 * (10 ** (-5))
    Rd = np.array([[r_theta, 0],                            # measurement covariance
                  [0, rw]])


    Ad = np.array([[1, 0, 0], [T, 1, 0], [0, 0, 1]])        # state transition model
    C = np.array([[0, 1, 0], [1, 0, 1]])                    # measurement matrix
    I = np.identity(dim)

    zero_mean = np.array([0.0, 0.0, 0.0])                   # to construct any N(0, Cov) 


    state_t = uniform_samples(a, b, n_samples, dim)         # initialising particles to span the limits of state
    # states_transpose = state_t.T


    particle_set_t = []                                                 # to hold the predicted particle set

    for n in range(n_samples):
        # predicted motion step:
        xn_t = state_t[n]                                               # nth particle state at time t
        motion_noise = np.random.multivariate_normal(zero_mean, Qd)     # adding motion noise ~ N(0, Qd)
        xn_t1 = np.dot(Ad, xn_t.T) + motion_noise                       # hypothetical nth particle state at time t + 1


        # measurement correction step:
        z_t = np.array([z_theta[n], z_dtheta[n]])
        exp_zt = np.dot(C, xn_t1)                                       # expected z_t for each hyp. particle x_t
        # obs_noise = np.random.multivariate_normal(exp_zt, Rd)           # adding measurement noise ~ N(Cxt, Rd)
        weight_xn_t1 = state_likelihood(z_t, exp_zt, Rd)

        print("Obs: {0} \t\tExp: {1} \t\tProb.: {2}".format(z_t, exp_zt, weight_xn_t1))

        particle_set_t.append([xn_t1, weight_xn_t1])
    
    # print(np.array(particle_set_t))

# TODO: 1. Move weighting process before prediction to go ahead with first un-intialized particles
# TODO: 2. Make weight and state matrices and then edit them only rather than appending to a new one.


if __name__ == "__main__":
    main()
