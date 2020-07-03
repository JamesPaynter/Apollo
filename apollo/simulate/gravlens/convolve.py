import numpy as np
import scipy.signal

import matplotlib.pyplot as plt

from apollo.simulate.qso.quasar import Quasar
from apollo.simulate.gravlens.magmap import MagnificationMap


def test_map():
    map = np.ones((100,100))
    return map

def test_quasar():
    qso = np.ones((20,20))
    return qso

class MapTransforms(object):
    """docstring for MapTransforms."""

    def __init__(self):
        super(MapTransforms, self).__init__()

    def rotate_map(self, map, angle):
        """ Implements rotation by area mapping.

        http://www.leptonica.org/rotation.html

        Parameters
        ----------
        map : 2D array
            The magnification map. A scalar field.
        angle : float
            The angle through which to rotate the map (clockwise).

        Returns
        -------
        map : 2D array
            The rotated magnification map. A scalar field.

        """
        pass

    def zoom_in_map(self, map, zoom_fraction):
        """ Make sure cannot zoom in past reasonable zoom.
        """
        pass

    def zoom_out_map(self, map, zoom_fraction):
        """ Make sure cannot zoom out past minimum zoom.
        """
        pass

class MapConvolution(MapTransforms):
    """docstring for MapConvolution.

    Returns
    -------

    convolution: array
        The source image convolved with a strip of the magnification map

    """

    def __init__(self, qso, map):#, map_angle, ):
        super(MapConvolution, self).__init__()

        self._test_quasar_type(qso)
        self._test_map_type(map)
        self.convolve()
        self.plot_conv()

    def _test_quasar_type(self, qso):
        """
        """
        try:
            qso = np.array(qso)
        except TypeError as error:
            print(error)
            print("The quasar should be a 2D+1 array of floats.")
        try:
            a, b = np.shape(qso)
            self.qso = qso[:, :, None]
        except:
            try:
                a, b, c = np.shape(qso)
            except:
                print("Quasar is the wrong shape.")
                print(f"The shape is {np.shape(map)}")
                print("Expected (n,n,z) or (n,n) -> (n,n,1).")
            self.qso = qso


    def _test_map_type(self, map):
        """
        """
        try:
            map = np.array(map)
        except TypeError as error:
            print(error)
            print("The map should be a 2D array of floats.")
        try:
            a, b = np.shape(map)
            self.map = map
        except:
            print("Magnification map is the wrong shape.")
            print(f"The shape is {np.shape(map)}")
            print("Expected (n,n)")


    def convolve(self):
        for i in range(len(self.qso[0,0,:])):
            print(self.qso[:,:,i])
            print(self.map)
            print(np.shape(self.qso[:,:,i]))

            print(np.shape(self.map))

            # ttype = 'valid'
            # ttype = 'full'
            ttype = 'same'
            self.conv = (scipy.signal.convolve(self.qso[:,:,i], self.map,
                                                mode = ttype)
                        / np.sum(self.map))
            print(self.conv)
            print(np.shape(self.conv))

    def plot_conv(self):
        plt.imshow(self.conv)
        plt.colorbar()
        plt.show()







if __name__ == '__main__':
    # map = test_map()
    # qso = test_quasar()
    # MapConvolution(qso, map)


    QSO = Quasar()
    map = MagnificationMap()
    # square = map.return_strip(0,0,0)
    MapConvolution(QSO.disk, map.map)
