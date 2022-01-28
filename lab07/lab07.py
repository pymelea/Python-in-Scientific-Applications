from numba import jit
import numpy as np
import random
import time


# Calculate current system energy
@jit(nopython=True, fastmath=True)
def calculate_energy(state: np.ndarray, size: int, J: float, H: float):
    # Interaction energy between neighbours
    nodes_energy = 0
    # Interaction energy with external field
    field_energy = 0
    # Full energy of system
    full_energy = 0

    for i in range(size):
        for j in range(size):
            s_u = state[(i + 1) % size, j]
            s_b = state[(i - 1) % size, j]
            s_l = state[i, (j - 1) % size]
            s_r = state[i, (j + 1) % size]
            s_c = state[i, j]
            nodes_energy += (s_u + s_b + s_l + s_r) * s_c

    field_energy = -H * np.sum(state)
    full_energy = -J * nodes_energy + field_energy
    return full_energy


# Calculate new spins configuration
@jit(nopython=True, fastmath=True)
def calculate_new_state(state: np.ndarray, size: int, beta: float):

    # As many cases as many spins
    for _ in range(size * size):

        # Calculate old energy without changed spin state
        old_energy = calculate_energy(state, size, J, H)

        # Random choice of spin
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)

        # Change spine state
        state[i, j] = -state[i, j]

        # Calculate new energy with changed spin state
        new_energy = calculate_energy(state, size, J, H)

        # If energy change < 0, then we accept spin change
        delta_energy = new_energy - old_energy

        # If energy change > 0, we unaccept spin change when...
        if delta_energy > 0:
            if random.random() > np.exp(-beta * delta_energy):
                state[i, j] = -state[i, j]


# Main simulation 
def simulation(state: np.ndarray, size: int, beta: float, N: int):
    for _ in range(N):
        calculate_new_state(state, size, beta)
    return new_state


# MAIN
if __name__ == '__main__':

    # state size
    size = 18
    # Exchange integral
    J = 0.7
    # Temperature
    beta = 0.1
    # Field value
    H = 2.5
    # Simulation steps
    N = 50

    # Set sign print option
    np.set_printoptions(formatter={'int': lambda x: "{:>+}".format(x)})

    # Create spins state 
    state = np.random.randint(2, size=(size, size), dtype=np.int8) * 2 - 1
    print(str(state).replace(' [', '').replace('[', '').replace(']', ''))
    print('\n')

    # Calculate new state
    new_state = state 
    start = time.time()
    new_state = simulation(new_state, size, beta, N)
    stop = time.time()
    print(str(new_state).replace(' [', '').replace('[', '').replace(']', ''))
    print('\n')
    print(f'Execution time: {(stop - start):.5f} sec.')

    # For parameters: size=18, J=0.7, beta = 0.1, H=2.5, N=50
    # With Numba:     0.796 s
    # Without Numba:  13.42 s
