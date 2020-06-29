import numpy as np
import matplotlib.pyplot as plt


def makemap(map_object, **kwargs):
    map = map_object.return_map(**kwargs)
    return map

class EmptyMap(object):
    """docstring for EmptyMap."""

    def __init__(self, ):
        super(EmptyMap, self).__init__()


class MagnificationMap(object):
    """docstring for MagnificationMap.

    Returns
    -------

    map: array
        A 2d array of the magnifications at each x,y coord to convolve with a
        source image.

    """

    def __init__(self, resolution = 1000):
        super(MagnificationMap, self).__init__()

        self.resolution = resolution
        self.map = self.makemap()

        self.plot_map()


    def toy_map(self, map):
        out = np.zeros((self.resolution, self.resolution))
        for xx in range(len(map[0,:])):
            for yy in range(len(map[:,0])):
                if yy - 0.5 * self.resolution + 1e-3 > 0:
                    out[xx,yy] = - (0.4*np.log(yy - 0.5 * self.resolution + 1e-3)
                                    - 4)
                                    # )
                else:
                    out[xx,yy] = 0
        return out


    def makemap(self):

        map = np.zeros((self.resolution, self.resolution))
        map = self.toy_map(map)

        return map

    def return_strip(self, start, width, axes):
        return

    def plot_map(self):
        plt.imshow(self.map)
        plt.colorbar()
        plt.show()




if __name__ == '__main__':
    map = MagnificationMap()
