"""
Artificial Images Simulator Class
===================================

The Artificial Images Simulator (AIS) class was developed to generate
artificial star images, similar to those images that would be acquired by
using the acquisition system of the instrument. To accomplish this,
the AIS models as star flux as a 2D gaussian distribution. Then, the star
flux is added to an image with a background level given by counts distribution
of an image of the SPARC4 cameras, as a function of its operation mode.
"""

# import read_noise_calc as RNC
# from photutils.datasets import make_noise_image
# import numpy as np
# import openpyxl

# from astropy.table import Table
# from photutils.datasets import make_gaussian_sources_image
# from sys import exit

from PSF import Point_Spread_Function
from BGI import Background_Image
from HDR import Header
from CHC import (Concrete_Channel_1,
                 Concrete_Channel_2,
                 Concrete_Channel_3,
                 Concrete_Channel_4)


__all__ = ['Artificial_Images_Simulator']


class Artificial_Images_Simulator:
    """Create an image cube with the star flux distribution.

    Parameters
    ----------
    star_flux : float
        Number of photons per second of the star
    sky_flux: float
        Number of photons per second of the sky
    gaussian_stddev: int
        Number of pixels of the gaussian standard deviation
    ccd_operation_mode: dictionary
        A python dictionary with the CCD operation mode. The allowed keywords
        values for the dictionary are

        * em_mode: {0, 1}

           Use the 0 for the Conventional Mode and 1 for the EM Mode

        * em_gain: float

           Electron Multiplying gain

        * preamp: {1, 2}

           Pre-amplification

        * hss: {0.1, 1, 10, 20, 30}

           Horizontal Shift Speed (readout rate) in MHz

        * bin: int

           Number of the binned pixels

        * t_exp: float

           Exposure time in seconds

    ccd_temp: float, optional
        CCD temperature

    serial_number: {9914, 9915, 9916 or 9917}, optional
        CCD serial number

    bias_level: int, optional
        Bias level, in ADU, of the image

    image_dir: str, optional
        Directory where the image should be saved


    Attribute
    ----------
    image_name: str
        Name of the image cube
    dark_current: float
        Dark current in e-/s/pix
    read_noise: float
        Read noise in e-/pix
    gain: float
        CCD pre-amplification gain in e-/ADU
    hdr: list
        Header content of the image


    Yields
    ------
        image cube: int
            An image cube in the FITS format with the star flux distribution

    Notes
    -----
        Explica o código; background; passo-a-passo

    Examples
    --------
        Incluir exemplos

    References
    ----------
    .. [#Bernardes_2018] Bernardes, D. V., Martioli, E., and Rodrigues, C. V., “Characterization of the SPARC4 CCDs”, <i>Publications of the Astronomical Society of the Pacific</i>, vol. 130, no. 991, p. 95002, 2018. doi:10.1088/1538-3873/aacb1e.

    """

    def __init__(self,
                 star_flux,
                 sky_flux,
                 gaussian_stddev,
                 ccd_operation_mode,
                 channel=1,
                 bias_level=500,
                 image_dir=''):
        """Initialize the class."""
        if type(star_flux) not in [int, float]:
            raise ValueError(f'The star flux must be a number: {star_flux}')
        elif star_flux > 0:
            self.star_flux = star_flux
        else:
            raise ValueError(
                f'The star flux must be greater than zero: {star_flux}')

        if type(sky_flux) not in [int, float]:
            raise ValueError(f'The sky flux must be a number: {sky_flux}')
        elif sky_flux > 0:
            self.sky_flux = sky_flux
        else:
            raise ValueError(
                f'The sky flux must be greater than zero: {sky_flux}')

        if type(gaussian_stddev) is not int:
            raise ValueError(
                f'The gaussian standard deviation must be an integer: {gaussian_stddev}')
        elif gaussian_stddev > 0:
            self.gaussian_stddev = gaussian_stddev
        else:
            raise ValueError(
                f'The gaussian standard deviation must be greater than zero: {gaussian_stddev}')

        self._verify_ccd_operation_mode(ccd_operation_mode)

        if channel in [1, 2, 3, 4]:
            self.channel = channel
        else:
            raise ValueError(
                f'There is no camera with the provided serial number: {channel}')

        if type(bias_level) is not int:
            raise ValueError(
                f'The bias level must be an integer: {bias_level}')
        elif bias_level >= 0:
            self.bias_level = bias_level
        else:
            raise ValueError(f'The bias level must be positive: {bias_level}')

        if type(image_dir) is not str:
            raise ValueError(
                f'The directory path must be a string: {image_dir}')
        else:
            if image_dir != '':
                if '\\' not in image_dir[-1]:
                    image_dir += '\\'
            self.image_dir = image_dir

        CHC = 0
        if channel == 1:
            CHC = Concrete_Channel_1()
        elif channel == 2:
            CHC = Concrete_Channel_2()
        elif channel == 3:
            CHC = Concrete_Channel_3()
        elif channel == 4:
            CHC = Concrete_Channel_4()
        self.CHC = CHC
        self.PSF = Point_Spread_Function(CHC)
        self.BGI = Background_Image(CHC)
        self.HDR = Header(ccd_operation_mode)
        self.image_name = ''
        self.dark_current = 0
        self.read_noise = 0
        self.gain = 0
        self.hdr = []

    def _verify_ccd_operation_mode(self, ccd_operation_mode):
        """Verify if the provided CCD operation mode is correct."""
        self.ccd_operation_mode = ccd_operation_mode
        dic_keywords_list = [
            'em_mode', 'em_gain', 'preamp', 'hss', 'bin', 't_exp', 'ccd_temp']
        for key in ccd_operation_mode.keys():
            if key not in dic_keywords_list:
                raise ValueError(
                    f'The name provided is not a CCD parameter: {key}')

        if list(ccd_operation_mode.keys()) != dic_keywords_list:
            raise ValueError(
                'There is a missing parameter of the CCD operation mode')

        if ccd_operation_mode['em_mode'] not in [0, 1]:
            raise ValueError(
                f'Invalid value for the EM mode: {ccd_operation_mode["em_mode"]}')
        if ccd_operation_mode['em_mode'] == 0:
            if ccd_operation_mode['em_gain'] != 1:
                raise ValueError(
                    f'For the Conventional Mode, the EM Gain must be 1: {ccd_operation_mode["em_gain"]}')
        else:
            if ccd_operation_mode['em_gain'] < 2 or ccd_operation_mode['em_gain'] > 300:
                raise ValueError(
                    f'EM gain out of range [2, 300]: {ccd_operation_mode["em_mode"]}')
        if ccd_operation_mode['preamp'] not in [1, 2]:
            raise ValueError(
                f'Invalid value for the pre-amplification: {ccd_operation_mode["preamp"]}')
        if ccd_operation_mode['hss'] not in [0.1, 1, 10, 20, 30]:
            raise ValueError(
                f'Invalid value for the Readout rate: {ccd_operation_mode["hss"]}')
        if ccd_operation_mode['bin'] not in [1, 2]:
            raise ValueError(
                f'Invalid value for the binning: {ccd_operation_mode["bin"]}')
        if ccd_operation_mode['t_exp'] < 1e-5:
            raise ValueError(
                f'Invalid value for the exposure time: {ccd_operation_mode["t_exp"]}')
        if ccd_operation_mode['ccd_temp'] < -80 or ccd_operation_mode['ccd_temp'] > 20:
            raise ValueError(
                f'CCD temperature out of range [-80, 20]: {ccd_operation_mode["ccd_temp"]}')

    def get_channel_ID(self):
        """Return the ID for the respective SPARC4 channel."""
        return self.CHC.get_channel_ID()

    def _configure_image_name(self, include_star_flux=False):
        """Create the image name.

        The image name will be created based on the provided information

        Parameters
        ----------
        include_star_flux: bool, optional
            Indicate if it is needed to include the star flux value in the
            image name
        """
        dic = self.ccd_operation_mode
        em_gain = '_G' + str(dic['em_gain'])
        em_mode = 'CONV'
        if dic['em_mode'] == 1:
            em_mode = 'EM'
        hss = '_HSS' + str(dic['hss'])
        preamp = '_PA' + str(dic['preamp'])
        binn = '_B' + str(dic['bin'])
        t_exp = '_TEXP' + str(dic['t_exp'])
        self.image_name = em_mode + hss + preamp + binn + t_exp + em_gain

        if include_star_flux:
            star_flux = '_S' + str(self.star_flux)
            self.image_name += star_flux

    def create_image(self):
        """Create the star image.

        This function will sum the background image with the star SPF image
        to create a artificil image, similar to those image acquired by the
        SPARC4 cameras.


        Returns
        -------
        Star Image:
            A FITS file with the calculated artificial image
        """
        pass
