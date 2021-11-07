# Import dependencies
import numpy as np
import random
from rich.progress import track
from PIL import Image


class Ising:

    # Constructor
    def __init__(self, size: int, J: float, beta: float, H: float, N: int):
        self.size = size
        self.J = J
        self.beta = beta
        self.H = H
        self.N = N
        self.frame = np.random.randint(2, size=(size, size)) * 2 - 1

    # Calculate current magnetisation
    def calculate_magnetisation(self):
        magnetisation = np.sum(self.frame)
        return magnetisation

    # Calculate current system energy
    def calculate_energy(self):

        # Interaction energy between neighbours
        nodes_energy = 0
        # Interaction energy with external field
        field_energy = 0
        # Full energy of system
        full_energy = 0

        for i in range(self.size):
            for j in range(self.size):

                s_u = self.frame[(i + 1) % self.size, j]
                s_b = self.frame[(i - 1) % self.size, j]
                s_l = self.frame[i, (j - 1) % self.size]
                s_r = self.frame[i, (j + 1) % self.size]
                s_c = self.frame[i, j]

                nodes_energy += (s_u + s_b + s_l + s_r) * s_c

        field_energy = -self.H * np.sum(self.frame)
        full_energy = -self.J * nodes_energy + field_energy
        return full_energy

    # Calculate new spins configuration
    def calculate_new_state(self):

        # As many cases as many spins
        for _ in range(self.size * self.size):

            # Calculate old energy without changed spin state
            old_energy = self.calculate_energy()

            # Random choice of spin
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)

            # Change spine state
            self.frame[i, j] = -self.frame[i, j]

            # Calculate new energy with changed spin state
            new_energy = self.calculate_energy()

            # If energy change < 0, then we accept spin change
            delta_energy = new_energy - old_energy

            # If energy change > 0, we unaccept spin change when...
            if delta_energy > 0:
                if random.random() > np.exp(-self.beta * delta_energy):
                    self.frame[i, j] = -self.frame[i, j]

    # Save image with spins
    def save_image(self, step, arrow_up, arrow_down, width, height, img):

        # Each step has own image
        filename = f'step_{step}.png'
        img.save(filename)

        # For each row and col, save arrow up if 1 or arrow down if -1
        for i in range(0, self.size):
            for j in range(0, self.size):
                out = Image.open(filename)
                if self.frame[i, j] == 1:
                    # the second argument here is tuple representing upper left corner
                    out.paste(arrow_up, (i * width, j * height))
                else:
                    out.paste(arrow_down, (i * width, j * height))
                out.save(filename)

    # Mainly simulation
    def simulation(self):

        file = open('magnetisation.txt', 'w')
        file.write('STEP\tM\n')

        # Initial magnetisiation
        magnetisation = 0

        # Read arrows and create empty image
        arrow_up = Image.open('arrow_u.png')
        arrow_down = Image.open('arrow_d.png')
        width, height = arrow_up.size
        img = Image.new('RGB', (width * self.size, height * self.size))

        for step in track(range(self.N), description='Processing...', auto_refresh=False):
            # Save before calculate new state because we want to have info about initial state
            self.save_image(step, arrow_up, arrow_down, width, height, img)
            magnetisation = self.calculate_magnetisation() / (self.size * self.size)
            file.write(f'{step}\t{magnetisation}\n')
            # New state
            self.calculate_new_state()

        file.write(f'{self.N}\t{magnetisation}\n')
        file.close()
        self.save_image(self.N, arrow_up, arrow_down, width, height, img)


# MAIN
if __name__ == '__main__':

    # Frame size
    size = 10
    # Exchange integral
    J = 0.5
    # Temperature
    beta = 0.25
    # Field value
    H = 1.5
    # Simulation steps
    N = 10

    # Create object and run simulation
    ising = Ising(size, J, beta, H, N)
    ising.simulation()
