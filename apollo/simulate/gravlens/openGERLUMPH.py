import numpy as np
import matplotlib.pyplot as plt

from apollo.simulate.gravlens.magmap import makemap

class OpenGERLUMPH(object):
    """docstring for OpenGERLUMPH."""

    def __init__(self, name):
        super(OpenGERLUMPH, self).__init__()

        self.name = name
        self.get_meta_data()

    def get_meta_data(self):
        self.metadata = {}
        key_words  = [  ['avg_mag', 'avg_rays_pp'],
                        ['resolution'],
                        ['map_width_er'],
                        ['convergence', 'shear', 'smooth_matter']
                    ]

        meta_file = f'maps/GERLUMPH/{self.name}/mapmeta.dat'
        with open(meta_file, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                words = line.split()
                for j, word in enumerate(words):
                    self.metadata[key_words[i][j]] = float(word)


    def open_map(self):
        filename = f'maps/GERLUMPH/{self.name}/map.BIN'
        with open(filename, "rb") as file:
            a = np.fromfile(file, dtype=np.uint32)
            map = np.reshape(a, (10000,10000))

        magnification = map * np.abs(   self.metadata['avg_mag']
                                      / self.metadata['avg_rays_pp'])

        plt.imshow(magnification)
        plt.colorbar()
        plt.show()



if __name__ == '__main__':

    aa = OpenGERLUMPH('k0610g0420s0900')
    aa.open_map()
