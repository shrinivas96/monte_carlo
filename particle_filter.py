import numpy as np
import pandas as pd
from filterpy import monte_carlo
import samples_and_measurements as sm

# Global contants for needed throughout
deg2rad = np.pi / 180
rad2deg = 180 / np.pi
T = 0.01                                                # sampling time. new measuements at every T seconds
I = np.identity(3)
zero_mean = np.array([0.0, 0.0, 0.0])                   # to construct any N(0, Cov) 
np.random.seed(0)


def state_likelihood(measurement_t, state_t):
    """
    Returns the multivariate gaussian likelihood of measurement_t given state_t.
    That is, p(z_t | x_t). x_t is the hypothetical state particle.

    Parameters:
    measurement_t: 2x1 vector of the observed measurement
    state_t: 2x1 vector of hypothetical state. 
    
    Returns the likelhood of z_t given x_t:
    L(z_t | x_t) = (2 pi)^(-k/2) * |cov|^(-1/2) * e ^ {-0.5 * (z - mu)^T . cov^(-1) . (z - mu)}
    """
    # constants for the measurement model
    rw = 10 ** (-6)                                 # uncetrainty in gyro measurements
    r_theta = 5 * (10 ** (-5))                      # uncertainty in accel. measurements
    Rd = np.array([[r_theta, 0],                    # measurement covariance
                   [0, rw]])
    C = np.array([[0, 1, 0], [1, 0, 1]])                    # measurement matrix


    # obs_noise = np.random.multivariate_normal(expected_zt, Rd)           # adding measurement noise ~ N(Cxt, Rd)

    expected_zt = np.dot(C, state_t)                                       # expected z_t for each hyp. particle x_t
    k = measurement_t.size                                    # dimension of the vector 
    e1 = (2 * np.pi) ** (-1/2)                      # first expression of likelihood

    cov_sqrt_det = np.linalg.det(Rd) ** (-1/2)     # square root of the determinant of covariance matrix
    cov_inverse = np.linalg.inv(Rd)                # inverse of the covariance matrix

    z_mean_diff = (measurement_t - expected_zt)                                                  # difference between observed and expected measurement
    z_mean_diff_T = (measurement_t - expected_zt).T                                              # transpose of above
    exponential = np.exp(-0.5 * (z_mean_diff_T @ cov_inverse @ z_mean_diff))    # exponential part of the likelihood function

    likelihood = e1 * cov_sqrt_det * exponential                                # the likelihood L(z_t)
    return likelihood


def sample_motion_model(particle_n):
    """
    Propagates particle_n through the motion model and adds a gaussian noise.
    
    Parameters:
    particle_n: Hypothetical state vector; i.e the nth particle at time t x^{[n]}_t 
    
    Returns xn_t1: state vector at time t+1 x^{[n]}_{t+1}
    """
    # contants and matrices for motion model
    qw = 5                                          # uncertainty in w := dtheta
    qb = 0.01                                       # uncertainty in bias 
    q_01 = (T ** 2) * qw / 2
    Qd = np.array([[T * qw, q_01, 0],               # motion covariance
                   [q_01, (T ** 3) * qw / 3, 0], 
                   [0, 0, T * qb]])
    Ad = np.array([[1, 0, 0], [T, 1, 0], [0, 0, 1]])        # state transition model
    
    motion_noise = np.random.multivariate_normal(zero_mean, Qd)     # adding motion noise ~ N(0, Qd)
    xn_t1 = np.dot(Ad, particle_n.T) + motion_noise                 # hypothetical nth particle state at time t + 1

    return xn_t1


def particle_filter(particle_set_t, measurement_t):
    """
    Bare-bones particle filter algorithm.
    Takes as input the particle set at this time step and returns the particle set at t+1.
    Parameters:

    particle_set_t: Array of vectors. Each vector is a state hypothesis and so is the same dimesion
    as the state itself.

    measurement_t: Array of the measurements [z_theta, z_dtheta]

    Returns: particle_set_t1: Array of vectors estimated to be the state in next time step
    """

    n_samples, dim = particle_set_t.shape           # the number of particles and dimension of each particle


    # predicted_belief = dict()
    # estimated_belief = dict()
    # bar_Xt = []
    # bar_Xt1 = np.empty((n_samples, 2))
    # bar_Xt2 = np.empty((n_samples, dim))
    # Attempts to save the particle and the weights in one place, or one array (inside for loop)
        # temp_arr = np.array([xn_t1, weight_xn_t1])
        # bar_Xt.append([xn_t1, weight_xn_t1])
        # bar_Xt1[n] = 0
        # bar_Xt2 = np.append(xn_t1, weight_xn_t1)
        # predicted_belief[xn_t1] = weight_xn_t1
    # bar_Xt = np.array(bar_Xt)                         # previous version used bar_Xt, array of array of particles and weights
    # weights = bar_Xt[:, 1]                            # to be uncommented if we are using bar_Xt

    weights = []
    pred_state = []
    est_state_set = []

    
    # this for-loop effectively calculates \bar{X_t}, i.e. the predicted belief.
    for n in range(n_samples):
        # predicted motion step:
        xn_t1 = sample_motion_model(particle_set_t[n])

        # measurement correction step:
        weight_xn_t1 = state_likelihood(measurement_t, xn_t1)

        pred_state.append(xn_t1)
        weights.append(weight_xn_t1)

        # print("Obs: {0} \t\tExp: {1} \t\tProb.: {2}".format(z_t, mean, weight_xn_t1))
    
    weights = np.array(weights)
    pred_state = np.array(pred_state)

    # the resampling step:
    indices = monte_carlo.residual_resample(weights)

    for index in indices:
        est_state_set.append(pred_state[index])

    return est_state_set


"""
for t in time will go in some main function and 
in each time step we will call the particle filter algorithm 
and pass it just the particle set and enw measurement step in that time step.
"""


# TODO: 1. Move weighting process before prediction to go ahead with first un-intialized particles
# TODO: 2. Make weight and state matrices and then edit them only rather than appending to a new one.


if __name__ == "__main__":
    a, b = -1.6, 0.8                    # interval to generate uniform particles
    n_samples = 10                     # number of samples
    dim = 3                             # vector dimension for 3 states to be estimated
    particle_set = sm.uniform_samples(a, b, n_samples, dim)         # initialising particles to span the limits of state

    # Actual measurements taken from the csv
    z_theta, z_dtheta = sm.retreive_measurement()              # unit rad, rad/sec
    time = len(z_theta)                 # total number of measurements that we have

    for t in range(time):
        z_t = np.array([z_theta[t], z_dtheta[t]])
        particle_set = particle_filter(particle_set, z_t)