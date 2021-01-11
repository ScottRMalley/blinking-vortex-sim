import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sim.abstract_sim import AbstractSim


class BlinkingVortexSim(AbstractSim):
    ###
    # Create a new blinking vortex
    #
    ###
    def __init__(self, mu, num_particles, expand_boundaries=False):
        # ensure particle number is even
        self.num_particles = (num_particles // 2) * 2
        self.mu = mu
        self.width = 2
        self.height = 1
        if expand_boundaries:
            self.width = 4
            self.height = 2
        self.right_vortex_pos = (1, 0)
        self.left_vortex_pos = (-1, 0)
        self.__initialize_particles()
        self.current_iteration = 0
        self.total_iterations = None
        super().__init__()

    def simulate(self, num_iterations, num_divisions, save_state=False, status_bar=False):
        self.total_iterations = 2 * num_iterations
        for i in range(num_iterations):
            # this is just to set the progress bar
            self.current_iteration = 2 * i

            # rotate right vortex
            self.__rotate_right_vortex(num_divisions, save_state, status_bar)

            # rotate left vortes
            self.current_iteration = 2 * i + 1
            self.__rotate_left_vortex(num_divisions, save_state, status_bar)

    def show(self):
        H, xedges, yedges = self.get_density_map(self.x_left, self.y_left, self.x_right, self.y_right)
        plt.imshow(H.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
        plt.show()

    def get_mixing(self):
        ms = []
        N = int(np.round(np.sqrt(self.num_particles))) // 8
        for frame in self.frames:
            x_left, y_left, x_right, y_right = frame
            xedges = np.linspace(-2, 2, 2 * N)
            yedges = np.linspace(-1, 1, N)
            H_left, xedges, yedges = np.histogram2d(x_left, y_left, bins=(xedges, yedges))
            H_right, xedges, yedges = np.histogram2d(x_right, y_right, bins=(xedges, yedges))
            H_diff = np.divide(np.absolute(H_left - H_right), H_left + H_right, out=np.ones_like(H_left),
                               where=((H_left + H_right) != 0))
            m = np.sum(np.sum(H_diff)) / float(len(xedges) * len(yedges))
            ms.append(m)
        cycles = np.linspace(0, self.total_iterations, len(self.frames))
        return cycles, ms

    def plot_mixing(self):
        cycles, mixing_parameter = self.get_mixing()
        plt.plot(cycles, mixing_parameter)
        plt.title('Mixing quantifier per cycle')
        plt.xlabel('cycles')
        plt.ylabel('mixing quantifier')
        plt.show()

    def get_density_map(self, x_left, y_left, x_right, y_right):
        N = int(np.round(np.sqrt(self.num_particles))) // 8
        xedges = np.linspace(-2, 2, 2 * N)
        yedges = np.linspace(-1, 1, N)
        H_left, xedges, yedges = np.histogram2d(x_left, y_left, bins=(xedges, yedges))
        H_right, xedges, yedges = np.histogram2d(x_right, y_right, bins=(xedges, yedges))
        H = H_right - H_left
        return H, xedges, yedges

    def get_state_image(self, frame_ind):
        x_left, y_left, x_right, y_right = self.frames[frame_ind]
        H, xedges, yedges = self.get_density_map(x_left, y_left, x_right, y_right)
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.imshow(H.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='upper')
        ax.set_title(r"Map $S_2$")
        canvas.draw()
        return np.array(canvas.renderer.buffer_rgba())

    def __save_state_to_frames(self):
        self.frames.append((self.x_left, self.y_left, self.x_right, self.y_right))

    def __initialize_particles(self):
        self.x_left = -self.width * np.random.rand(self.num_particles // 2)
        self.x_right = self.width * np.random.rand(self.num_particles // 2)
        self.y_left = self.height * (2 * np.random.rand(self.num_particles // 2) - 1.0)
        self.y_right = self.height * (2 * np.random.rand(self.num_particles // 2) - 1.0)

    def __rotate_vortex(self, num_divisions, vortex, save_state, status_bar):
        step = self.mu / float(num_divisions)
        for i in range(num_divisions):

            x_left, y_left = self.__calculate_new_position(self.x_left, self.y_left, vortex, step)
            self.x_left = x_left
            self.y_left = y_left

            x_right, y_right = self.__calculate_new_position(self.x_right, self.y_right, vortex, step)
            self.x_right = x_right
            self.y_right = y_right

            if save_state:
                self.__save_state_to_frames()
            if status_bar:
                self.print_status_bar(num_divisions * self.current_iteration + i,
                                      num_divisions * self.total_iterations - 1,
                                      prefix='Simulation progress')

    def __rotate_right_vortex(self, num_divisions, save_state=False, status_bar=False):
        self.__rotate_vortex(num_divisions, self.right_vortex_pos, save_state, status_bar)

    def __rotate_left_vortex(self, num_divisions, save_state=False, status_bar=False):
        self.__rotate_vortex(num_divisions, self.left_vortex_pos, save_state, status_bar)

    def __calculate_new_position(self, x, y, vortex_pos, step):
        d = (x - vortex_pos[0]) ** 2 + (y - vortex_pos[1]) ** 2
        theta = (step * self.mu) / d
        x_new = np.cos(theta) * (x - vortex_pos[0]) - np.sin(theta) * (y - vortex_pos[1]) + vortex_pos[0]
        y_new = np.sin(theta) * (x - vortex_pos[0]) + np.cos(theta) * (y - vortex_pos[1]) + vortex_pos[1]
        return x_new, y_new
