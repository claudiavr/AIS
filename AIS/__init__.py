# -*- coding: utf-8 -*-

"""Artificial Image Simulator of the SPARC4 instrument.

The AIS was developed to create cubes of artificial star images, simulating
those images that would be acquired by using the SPARC4 1 CCD cameras in
astronomical observations. To create the images, the AIS models the star
flux distribution as a 2D-Gaussian Distribution. This result is added to a
noise image, created based on the noise information of the SPARC4 CCDs, as
a function of their operation mode.
"""

from AIS import Artificial_Images_Simulator
from PSF import Point_Spread_Function
from BGI import Back_Ground_Image
from HDR import Header
