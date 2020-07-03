import numpy as np
import matplotlib.pyplot as plt

import sys
MIN_FLOAT = sys.float_info[3]


class FunSources(object):
    """docstring for FunSources."""

    def __init__(self):
        super(FunSources, self).__init__()

    def make_circle(self):
        # Source parameters
        xpos = 0   # Source position. X coordinate
        ypos = 0 # Source position. Y coordinate
        rad  = 0.1 # Radius of source
        ipos=   xpos / self.s_size # Convert source parameters to pixels
        jpos= - ypos / self.s_size
        rpix=   rad  / self.s_size
        # ipos=int(round(xpos/ys)) # Convert source parameters to pixels
        # jpos=int(round(-ypos/ys))
        # rpix=int(round(rad/ys))
        #
        circle = gaussian_ellipse( x = jpos, y = ipos,
                                    sigma_x = rpix, sigma_y = rpix,
                                    Npix = self.Ns_pix, theta = np.pi / 4)
        return circle

    def make_five_ellipse(self):
        xpos = 0   # Source position. X coordinate
        ypos = 0 # Source position. Y coordinate
        rad  = 0.1 # Radius of source
        ipos=   xpos / self.s_size # Convert source parameters to pixels
        jpos= - ypos / self.s_size
        rpix=   rad  / self.s_size


        x_array = [-0.6, -0.3, 0.0, 0.3, 0.6]
        source = np.zeros((self.Ns_pix, self.Ns_pix))
        for i, x_pos in enumerate(x_array):
            source += gaussian_ellipse( x = ipos + x_pos / self.s_size,
                                        y = jpos,
                                        sigma_x = rpix, sigma_y = rpix * 4,
                                        Npix = self.Ns_pix, theta = np.pi / 4)
        return source

    def make_uniform_field(self, n_source, radius_mean, radius_sigma):
        xpos = 0 # Source position. X coordinate
        ypos = 0 # Source position. Y coordinate
        rad  = 1 # Radius of source
        # Convert source parameters to pixels
        ipos=   xpos / self.s_size
        jpos= - ypos / self.s_size
        rpix=   rad  / self.s_size

        x_arr = 4 * np.random.rand(n_source) - 2
        y_arr = 4 * np.random.rand(n_source) - 2
        sigma_x = np.random.normal(radius_mean, radius_sigma, n_source)
        sigma_y = np.random.normal(radius_mean, radius_sigma, n_source)
        theta_array = np.pi * (2 * np.random.rand(n_source) - 1)
        source = np.zeros((self.Ns_pix, self.Ns_pix))
        for i, x_pos in enumerate(x_arr):
            source += gaussian_ellipse( x = x_arr[i] / self.s_size,
                                        y = y_arr[i] / self.s_size,
                                        sigma_x = rpix * sigma_x[i],
                                        sigma_y = rpix * sigma_y[i],
                                        Npix    = self.Ns_pix,
                                        theta   = theta_array[i],
                                        normed  = False)
        return source


def gaussian_ellipse(x, y, sigma_x, Npix, sigma_y = None, theta = 0, normed = True):
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
    # normalise to 1
    if normed:
        ellipse = ellipse / np.sum(ellipse)
    return ellipse

def point_lenses(x_s, y_s, x_l, y_l, m_l):
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

    The function returns the image position vector :math:`\Vec{y}`.

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

    x = x_s - x_l
    y = y_s - y_l
    r_squared = np.square(x) + np.square(y) + MIN_FLOAT
    alpha_x, alpha_y = m_l * x / r_squared, m_l * y / r_squared
    return x_s - alpha_x , y_s - alpha_y

    # def _make_array(parameter):
    #     if not isinstance(parameter, (list, np.ndarray)):
    #         try:
    #             parameter = np.array([parameter])
    #         except TypeError as error:
    #             print(error)
    #     return parameter
    # x_s = _make_array(x_s)
    # y_s = _make_array(y_s)
    # x_l = _make_array(x_l)
    # y_l = _make_array(y_l)
    # m_l = _make_array(m_l)
    #
    # def alpha_x_y(x_s, y_s, x_l, y_l, m_l):
    #     x = x_s - x_l
    #     y = y_s - y_l
    #     r_squared = np.square(x) + np.square(y) + MIN_FLOAT
    #     return m_l * x / r_squared, m_l * y / r_squared
    #
    # alpha_x, alpha_y = np.zeros(np.shape(x_s)), np.zeros(np.shape(x_s))
    # for i in range(len(m_l)):
    #     alpha_x_i, alpha_y_i = alpha_x_y(x_s, y_s, x_l[i], y_l[i], m_l[i])
    #     alpha_x += alpha_x_i
    #     alpha_y += alpha_y_i
    #
    # return x_s - alpha_x , y_s - alpha_y

class RayShooter(FunSources):
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

        source = self.make_five_ellipse()
        source = self.make_uniform_field(15, .1, .05)
        a, b = self.shoot_rays(source = source, lens = point_lenses)
        self.plot_rays(a, b)



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

    def shoot_rays(self, source, lens):
        # Lens parameters
        xd = 0
        yd = 0
        ml = 1
        xd = 2 * np.random.rand(2) - 1
        yd = 2 * np.random.rand(2) - 1
        ml = np.ones(2) / 3

        # This is the image plane, creates an empty 2D array
        image = np.zeros((self.Ni_pix,self.Ni_pix))
        # # create array of x,y pixels in image plane
        x1 = self.i_size * np.arange(self.Ni_pix) - self.i_len
        x2 = self.i_size * np.arange(self.Ni_pix) - self.i_len
        # turns into 2D array
        X1, X2 = np.meshgrid(x1, x2)
        # return a 2D array in the source plane
        # y1, y2 = lens(X1,X2,xd,yd,ml)
        y1, y2 = lens(X1,X2,0,0,1)
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
    rays = RayShooter(5001, 2)
