import numpy as np
import matplotlib.pyplot as plt

import sys
MIN_FLOAT = sys.float_info[3]




def gaussian_ellipse(x, y, sigma_x, Npix, sigma_y = None, theta = 0):
    # https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
    """
    Assumes the ellipse is to be calculated on a *square* pixel grid.

    Parameters
    ----------

    x, y : float
        The (x, y) coordinates of the Gaussian disk in the source plane.
    sigma_x, sigma_y: float
        The standard deviations of the Gaussian disk.
    theta : float
        Rotate the ellipse by theta radians clockwise relative to the x-y
        coordinates in the source plane.
    Npix : int
        The number of pixels in the source plane.


    Returns
    -------
    disk : ndarray
        A guassian disk.
    """
    if not sigma_y: sigma_y = sigma_x
    # meshgrid of x and y coords
    x_mesh, y_mesh = np.mgrid[0:Npix, 0:Npix]

    a = ( (np.cos(theta) ** 2) / (2 * sigma_x ** 2)
        + (np.sin(theta) ** 2) / (2 * sigma_y ** 2) )
    b = (  np.sin(theta   * 2) / (4 * sigma_y ** 2)
        -  np.sin(theta   * 2) / (4 * sigma_x ** 2) )
    c = ( (np.sin(theta) ** 2) / (2 * sigma_x ** 2)
        + (np.cos(theta) ** 2) / (2 * sigma_y ** 2) )

    ellipse = np.exp(-(a * np.square(x_mesh - x - Npix / 2)
                     + c * np.square(y_mesh - y - Npix / 2)
                     + 2 * b * (x_mesh - x - Npix / 2) * (y_mesh - y - Npix / 2)
                    ))
    ellipse = ellipse / np.sum(ellipse) # normalise to 1
    return ellipse

# from numba import njit
#
# @njit
def point(x_s, y_s, x_l, y_l, m_l):
    r"""
    Calculates the deflection angle as a function of position for a point mass
    gravitational lens.

    The gravitational lens equation can be expressed as

    .. math::

        \Vec{y} = \Vec{x} - \Vec{\alpha(\Vec{x})}

    Where :math:`\Vec{x}` are the coordinates in the source frame, expressed
    through the input parameters `x_s`, `y_s`. The deflection angle is

    .. math::

        \Vec{\alpha}(\Vec{x}) = M_\text{lens}
        \frac{\Vec{x} - \Vec{x}_d}{|\Vec{x} - \Vec{x}_d|^2}

    The function returns the image position vector :math:`\Vec{y}` expressed
    through the return parameters `x_i`, `y_i`.

    Parameters
    ----------
    x_s, y_s : float, array_like, meshgrid
        Source pixels.
    x_l, y_l : float
        Position of lens in image (lens) plane.
    m_l : float
        The lens mass. (in units of ?)


    Returns
    -------
    x_i, y_i

    """
    try:
        x_s = np.array(x_s)
    except TypeError as error:
        print(error)
        print("The source x-pixel position(s) should be a float or an array of")
        print("floats.")
    try:
        y_s = np.array(y_s)
    except TypeError as error:
        print(error)
        print("The source y-pixel position(s) should be a float or an array of")
        print("floats.")

    x = x_s - x_l # Distance along x axis of ray to lens position
    y = y_s - y_l # Distance along y axis of ray to lens position
    r_squared = np.square(x) + np.square(y) + MIN_FLOAT
    x_i = x_s - m_l * x / r_squared
    y_i = y_s - m_l * y / r_squared
    return x_i, y_i

class RayShooter(object):
    """docstring for RayShooter.

    Parameters
    ----------
    Ni_pix : int
        The number of pixels in the image plane.
    Ns_pix : int
        The number of pixels in the source plane. Optional.
        Default same as Ni_pix.
    i_len : float
        The length of the image plane in Einstein radii
    s_len : float
        The length of the source plane in Einstein radii. Optional.
        Default same as i_len.

    """

    def __init__(self,  Ni_pix, # Number of pixels in image plane
                        i_len, # half size of image plane covered (in "Einstein" radii)
                        Ns_pix = None, # Number of pixels in source plane
                        s_len = None,  # half size of source plane covered (in Einstein radii)
                        **kwargs):
        super(RayShooter, self).__init__()


        self.Ni_pix = Ni_pix
        self.Ns_pix = Ni_pix if not Ns_pix else Ns_pix
        self.i_len = i_len
        self.s_len = i_len if not s_len else s_len

        self.i_size = 2 * self.i_len / (self.Ni_pix - 1) # pixel size on the image map
        self.s_size = 2 * self.s_len / (self.Ns_pix - 1) # pixel size on the source map

        source = self.make_source()
        a, b = self.shoot_rays(source = source)
        self.plot_rays(a, b)

    def make_source(self):
        # Source parameters
        xpos = 0   # Source position. X coordinate
        ypos = 0.2 # Source position. Y coordinate
        rad  = 0.05 # Radius of source
        ipos=   xpos / self.s_size # Convert source parameters to pixels
        jpos= - ypos / self.s_size
        rpix=   rad  / self.s_size
        # ipos=int(round(xpos/ys)) # Convert source parameters to pixels
        # jpos=int(round(-ypos/ys))
        # rpix=int(round(rad/ys))

        ellipse = gaussian_ellipse( x = jpos, y = ipos,
                                    sigma_x = rpix, sigma_y = rpix,
                                    Npix = self.Ns_pix, theta = np.pi / 4)
        ellipse += gaussian_ellipse( x = jpos, y = ipos + 0.2 / self.s_size,
                                    sigma_x = rpix, sigma_y = rpix * 4,
                                    Npix = self.Ns_pix, theta = np.pi / 4)
        ellipse += gaussian_ellipse( x = jpos, y = ipos - 0.2 / self.s_size,
                                    sigma_x = rpix, sigma_y = rpix * 4,
                                    Npix = self.Ns_pix, theta = np.pi / 4)
        return ellipse

    def get_magnification(self, source, image, s_pix_area, i_pix_area):
        """
        The magnification is the ratio of the flux in the image plane to that
        in the source plane.

        When doing this numerically, the size of the pixels in each frame must
        be accounted for.

        PUT IN MASKS TO GET MAGNIFCATION OF DIFFERENT PARTS OF SOURCE



        Returns
        -------
        magnificaiton : float

        """
        print(np.sum(source), np.sum(image), np.sum(image)/np.sum(source))

    def shoot_rays(self, source, lens = point):
        # Lens parameters
        xd = 0
        yd = 0
        ml = 1

        # This is the image plane, creates an empty 2D array
        image = np.zeros((self.Ni_pix,self.Ni_pix))
        # # create array of x,y pixels in image plane
        x1 = self.i_size * np.arange(self.Ni_pix) - self.i_len
        x2 = self.i_size * np.arange(self.Ni_pix) - self.i_len
        # turns into 2D array
        X1, X2 = np.meshgrid(x1, x2)
        # return a 2D array in the source plane
        y1, y2 = lens(X1,X2,xd,yd,ml)
        # coordinates of deflected rays
        # i1, i2 are a set of indices
        i2 = np.round((y1+self.s_len)/self.s_size, 0).astype(int)
        i1 = np.round((y2+self.s_len)/self.s_size, 0).astype(int)
        # deflected rays within the bounds of the source box
        i2 = np.clip(i2, 0, self.Ni_pix - 1)
        i1 = np.clip(i1, 0, self.Ni_pix - 1)
        i = np.meshgrid(np.arange(self.Ni_pix))
        image = source[i1,i2]
        return source, image

    def plot_rays(self, a, b):
        # Plot stuff
        plt.subplot(121)
        plt.imshow(a,extent=(-self.s_len,self.s_len,-self.s_len,self.s_len), cmap = 'afmhot')
        plt.subplot(122)
        plt.imshow(b,extent=(-self.i_len,self.i_len,-self.i_len,self.i_len), cmap = 'afmhot')
        plt.show()


if __name__ == '__main__':
    rays = RayShooter(2001, 2)
