import numpy as np
import scipy

import matplotlib.pyplot as plt

from apollo.simulate.qso.quasar import Quasar
from apollo.simulate.gravlens.magmap import MagnificationMap





class MapConvolution(Quasar, MagnificationMap):
    """docstring for MapConvolution.

    Returns
    -------

    convolution: array
        The source image convolved with a strip of the magnification map

    """

    def __init__(self):
        super(MapConvolution, self).__init__()


        self.conv = scipy.signal.convolve(self.disk, self.map, 'valid')
        self.plot_map()

    def plot_map(self):
        plt.imshow(self.conv)
        plt.colorbar()
        plt.show()







if __name__ == '__main__':
    QSO = Quasar()
    map = MagnificationMap()
    square = map.return_strip(length = 0)
    MapConvolution(QSO.disk, square)
