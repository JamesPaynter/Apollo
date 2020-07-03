import numpy as np
import matplotlib.pyplot as plt

class Quasar(object):
    """
    docstring for Quasar.

    Returns
    -------
    disk: array
        A flattened 2D array of the quasar to convolve with a magnification map.

    """

    def __init__(self):
        super(Quasar, self).__init__()

        self.disk = None
        self.radius = 500 # pixels
        self.disk = self.disk_maker()
        # self.plot_disk()

    def solid_disk(self, disk):
        out = np.zeros((2*self.radius+1, 2*self.radius+1))
        for xx in range(len(disk[0,:])):
            for yy in range(len(disk[:,0])):
                out[xx,yy] = 0 if (xx-self.radius)**2 + (yy-self.radius)**2 > self.radius**2 else 1
        return out

    def disk_maker(self):
        disk = np.zeros((2*self.radius+1, 2*self.radius+1))
        disk = self.solid_disk(disk)
        return disk

    def flatten(self):
        pass

    def plot_disk(self):
        plt.imshow(self.disk)
        plt.show()


if __name__ == '__main__':
    QSO = Quasar()
