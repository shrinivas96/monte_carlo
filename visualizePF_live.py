import numpy as np
import matplotlib.pyplot as plt
import samples_and_measurements as sm
from matplotlib.animation import FuncAnimation

directory = "./particle_dataset/particle_set_"


def generator():
    # print(2, end="")
    theta_true, dtheta_true = sm.retreive_data(1)  # validation data; unit rad, rad/sec
    for t in range(1000):
        filename = directory + str(t)
        particle_set = np.loadtxt(filename)
        theta_est = particle_set[:, 1]
        dtheta_est = particle_set[:, 0]

        yield t, theta_est, dtheta_est, theta_true[t], dtheta_true[t]


def animator(data, scat1, scat2):
    # print(1, end="")
    t, theta, dtheta, theta_true, dtheta_true = data
    pos = t * np.ones(len(theta))
    true = np.c_[t, theta_true]

    estimate = np.c_[pos, theta + (np.pi / 2)]
    scat1.set_offsets(estimate)
    scat2.set_offsets(true)


def main():
    fig, ax = plt.subplots()
    ax.set_title(r"Particle Filter estimate of tilt angle $\theta$")
    ax.set(xlabel="Number of observations", ylabel="Tilt Angle $\theta$ ($rad$)")
    ax.grid()
    ax.set(xlim=(-1, 1001), ylim=(-3, 3))
    scat1 = ax.scatter([], [], s=3, color="blue")
    scat2 = ax.scatter([], [], s=20, color="red")
    ani = FuncAnimation(fig=fig,
                        func=animator,
                        frames=generator,
                        fargs=(scat1, scat2),
                        interval=2000)

    plt.show()


if __name__ == "__main__":
    main()
    # particle_set = np.loadtxt("./particle_dataset/particle_set_400")
    # theta_est = particle_set[:, 1]
    # dtheta_est = particle_set[:, 0]
    # theta_true, dtheta_true = sm.retreive_data(1)               # validation data; unit rad, rad/sec
    # fig, ax = plt.subplots()
    # scat = ax.scatter(np.arange(1000), theta_true, s=10, color='blue')
    # plt.show()
