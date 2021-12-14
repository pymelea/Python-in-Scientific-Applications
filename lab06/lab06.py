import numpy as np
import matplotlib.pyplot as plt
import time
from numba import jit
from functools import wraps
from statistics import mean


# This decorator may be launched with or without parameters
# The default runtime will give the function execution time
# You can also specify the number of times the function is repeated
# Then you get average execution time
def my_timer(*args_timer, **kwargs_timer):

    # Default option without arguments
    if len(args_timer) == 0 and len(kwargs_timer) == 0:
        def decorator(my_func):

            @wraps(my_func)
            def wrapper(*args_func, **kwargs_func):
                start = time.time()
                my_func(*args_func, **kwargs_func)
                stop = time.time()
                print(
                    f'{my_func.__name__} execution time: {(stop - start):.5f} sec.')

            return wrapper
        return decorator

    # Main option with arguments
    else:
        def decorator(my_func):
            times_table = []

            @wraps(my_func)
            def wrapper(*args_func, **kwargs_func):

                for _ in range(*args_timer):
                    start = time.time()
                    my_func(*args_func, **kwargs_func)
                    stop = time.time()
                    times_table.append(stop - start)
                print(
                    f'{my_func.__name__} average execution time: {mean(times_table):.5f} sec.')

            return wrapper
        return decorator


# Function it is compiled to machine code “just-in-time”
@jit(nopython=True, fastmath=True)
def sim_loop(Psi_R, Psi_I, H_R, H_I, norm, x_mean, energy, S, S_out, x, dx, tau, W, t, K):

    for i in range(1, S + 1):

        Psi_R = Psi_R + H_I * 0.5 * tau

        H_R[1:-1] = -0.5 * (Psi_R[:-2] + Psi_R[2:] - 2 * Psi_R[1:-1]) / \
            (dx * dx) + K * (x[1:-1] - 0.5) * \
            Psi_R[1:-1] * np.sin(W * (t + i * tau))

        Psi_I = Psi_I - H_R * tau

        H_I[1:-1] = -0.5 * (Psi_I[:-2] + Psi_I[2:] - 2 * Psi_I[1:-1]) / \
            (dx * dx) + K * (x[1:-1] - 0.5) * \
            Psi_I[1:-1] * np.sin(W * (t + i * tau))

        Psi_R = Psi_R + H_I * 0.5 * tau

        if i % S_out == 0:

            k = int(i / 1000)
            norm[k] = np.sum(dx * (Psi_R * Psi_R + Psi_I * Psi_I))
            x_mean[k] = np.sum(dx * x * (Psi_R * Psi_R + Psi_I * Psi_I))
            energy[k] = np.sum(dx * (Psi_R * H_R + Psi_I * H_I))


def draw_plot(times, x_mean, energy):

    plt.style.use("bmh")

    # Tworzymy subplot
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1,
                                   sharex=True, figsize=(10, 4.5), dpi=100)

    ax1.plot(times, x_mean, color="blue", alpha=0.75,
             linewidth=0.5, label="x mean")
    ax1.set_title("Quantum particle's mean position and energy",
                  fontname="Times New Roman", fontsize=16)
    ax1.set_ylabel("Mean Position", fontname="Times New Roman")

    ax2.plot(times, energy, color="blue", alpha=0.75,
             linewidth=2.0, label="energy")
    ax2.set_xlabel("Time", fontname="Times New Roman")
    ax2.set_ylabel("Energy", fontname="Times New Roman")

    fig.savefig('quantum.png', dpi=200)


@my_timer(2)
def main():
    # ----------------------------------------------------------------
    # Read data from file
    with open("parameters_py.txt", "r") as f:
        data = f.read()

    # We take only values
    data = data.split()
    data = data[0::2]

    # Change types to int or float
    data = (int(i) if i.isdigit() else float(i) for i in data)

    # Unzip values to variables
    N, n, m, omega, K, t, tau, S, S_out = data
    PI = np.pi
    W = omega * 0.01 * abs(m * m - n * n) * PI * PI * 0.5
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Initial conditions
    # Position
    x = np.linspace(0, 1, N + 1, dtype=float)

    # Real part of the wave function
    Psi_R = np.array(np.sqrt(2) * np.sin(n * PI * x), dtype=float)
    # Imagine part of the wave function
    Psi_I = np.zeros(N + 1, dtype=float)

    # Real part of the Hamiltonian function
    H_R = np.zeros(N + 1, dtype=float)
    # Imagine part of the Hamiltonian function
    H_I = np.zeros(N + 1, dtype=float)

    # Segment discretisation
    dx = 1.0 / N

    # Hamiltonian operator actions on the wave function
    H_R[1:-1] = -0.5 * (Psi_R[:-2] + Psi_R[2:] - 2 * Psi_R[1:-1]) / \
        (dx * dx) + K * (x[1:-1] - 0.5) * Psi_R[1:-1] * np.sin(W * t)

    H_I[1:-1] = -0.5 * (Psi_I[:-2] + Psi_I[2:] - 2 * Psi_I[1:-1]) / \
        (dx * dx) + K * (x[1:-1] - 0.5) * Psi_I[1:-1] * np.sin(W * t)

    # Initial informations about particle
    norm_0 = np.sum(dx * (Psi_R * Psi_R + Psi_I * Psi_I))
    x_mean_0 = np.sum(dx * x * (Psi_R * Psi_R + Psi_I * Psi_I))
    energy_0 = np.sum(dx * (Psi_R * H_R + Psi_I * H_I))

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Simulation
    # Arrays to plots
    k = int(S / S_out) + 1
    norm = np.empty(k, dtype=float)
    x_mean = np.empty(k, dtype=float)
    energy = np.empty(k, dtype=float)
    times = np.linspace(0, 50, k, dtype=float)

    # Zero-element is a initial information
    norm[0] = norm_0
    x_mean[0] = x_mean_0
    energy[0] = energy_0

    # Simulation loop
    sim_loop(Psi_R, Psi_I, H_R, H_I, norm, x_mean,
             energy, S, S_out, x, dx, tau, W, t, K)
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Plots
    draw_plot(times, x_mean, energy)
    # ----------------------------------------------------------------


# Main
if __name__ == '__main__':
    main()

# We see average time execution with numbs is aroud 3 seconds
# In turn without numba this time is around 20 seconds
