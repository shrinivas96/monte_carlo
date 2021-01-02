import numpy as np
import pandas as pd
import samples_and_measurements as sm

# Global contants for needed throughout
deg2rad = np.pi / 180
rad2deg = 180 / np.pi
T = 0.01                                        # sampling time. new measuements at every T seconds
I = np.identity(3)
zero_mean = np.array([0.0, 0.0, 0.0])                   # to construct any N(0, Cov) 


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


def sample_motion_model(particle_n):
    # contants and matrices for motion model
    qw = 5                                          # uncertainty in w := dtheta
    qb = 0.01                                       # uncertainty in bias 
    q_01 = (T ** 2) * qw / 2
    Qd = np.array([[T * qw, q_01, 0],               # motion covariance
                   [q_01, (T ** 3) * qw / 3, 0], 
                   [0, 0, T * qb]])
    Ad = np.array([[1, 0, 0], [T, 1, 0], [0, 0, 1]])        # state transition model
    
    print(particle_n)
    xn_t = particle_n                                               # nth particle state at time t
    motion_noise = np.random.multivariate_normal(zero_mean, Qd)     # adding motion noise ~ N(0, Qd)
    xn_t1 = np.dot(Ad, xn_t.T) + motion_noise                       # hypothetical nth particle state at time t + 1

    return 0


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


    # constants for process and measurement model

    rw = 10 ** (-6)                                 # uncetrainty in gyro measurements
    r_theta = 5 * (10 ** (-5))                      # uncertainty in accel. measurements
    Rd = np.array([[r_theta, 0],                    # measurement covariance
                   [0, rw]])
    C = np.array([[0, 1, 0], [1, 0, 1]])                    # measurement matrix

    predicted_belief = {}
    estimated_belief = {}

    
    
    for n in range(n_samples):
        # predicted motion step:
        xn_t1 = sample_motion_model(particle_set_t[n])

        # measurement correction step:
        z_t = np.array([z_theta[n], z_dtheta[n]])
        exp_zt = np.dot(C, xn_t1)                                       # expected z_t for each hyp. particle x_t
        # obs_noise = np.random.multivariate_normal(exp_zt, Rd)           # adding measurement noise ~ N(Cxt, Rd)
        weight_xn_t1 = state_likelihood(z_t, exp_zt, Rd)

        print("Obs: {0} \t\tExp: {1} \t\tProb.: {2}".format(z_t, exp_zt, weight_xn_t1))
    
    return 0


"""
for t in time will go in some main function and 
in each time step we will call the particle filter algorithm 
and pass it just the particle set and enw measurement step in that time step.
"""

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
    z_theta, z_dtheta = sm.retreive_measurement()              # unit rad, rad/sec
    rw = 10 ** (-6)
    r_theta = 5 * (10 ** (-5))
    Rd = np.array([[r_theta, 0],                            # measurement covariance
                  [0, rw]])


    Ad = np.array([[1, 0, 0], [T, 1, 0], [0, 0, 1]])        # state transition model
    C = np.array([[0, 1, 0], [1, 0, 1]])                    # measurement matrix

    zero_mean = np.array([0.0, 0.0, 0.0])                   # to construct any N(0, Cov) 


    state_t = sm.uniform_samples(a, b, n_samples, dim)         # initialising particles to span the limits of state


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
    a, b = -0.5, 0.5                    # interval to generate uniform particles
    n_samples = 10                     # number of samples
    dim = 3                             # vector dimension for 3 states to be estimated
    particle_set = sm.uniform_samples(a, b, n_samples, dim)         # initialising particles to span the limits of state

    # Actual measurements taken from the csv
    z_theta, z_dtheta = sm.retreive_measurement()              # unit rad, rad/sec
    time = len(z_theta)                 # total number of measurements that we have

    for t in range(time):
        z_t = np.array([z_theta[t], z_dtheta[t]])
        particle_set = particle_filter(particle_set, z_t)
