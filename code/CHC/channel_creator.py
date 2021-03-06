# -*- coding: utf-8 -*-

"""
Channel Creator
===============

This class creates the several channels of the SPARC4. The AIS is based on the
Factory Method to implement the correct star flux calculation as a function of
the optical path of each channel. This package has as abstract class that will
be provided to the Point_Spread_Function Class. Then, the Point_Spread_Function
class will call the correct concrete channel creator for the respective desired
image.
"""

import numpy as np
from RNC import Read_Noise_Calculation
from S4_SR import Abstract_SPARC4_Spectral_Response


class Abstract_Channel_Creator:
    """Abstract Channel Creator Class.

    This is an abstracty class that represents the SPARC4 channels. It is
    responsible to calculate the star or the sky flux as a function of the
    properly instrumental response of the SPARC4 channel.

    Parameters
    ----------
    ccd_temp : float
        The CCD temperature in ºC
    sparc4_acquisition_mode : [phot, pol]
        Acquisition mode of the SPARC4: photometric or polarimetric
    """

    _CHANNEL_ID = 0
    _SERIAL_NUMBER = 0

    def __init__(self, ccd_temp, sparc4_acquisition_mode):
        """Initialize the class."""
        self.ccd_temp = ccd_temp
        self.sparc4_acquisition_mode = sparc4_acquisition_mode

    def _factory_method(self):
        pass

    def get_channel_ID(self):
        """Return the Channel ID."""
        return f"Channel {self._CHANNEL_ID}"

    def get_serial_number(self):
        """Return CCD serial number.

        Returns
        -------
        _serial_number: 9914, 9915, 9916, 9917
            Serial number of the CCD

        """
        return self._SERIAL_NUMBER

    def calculate_dark_current(self):
        """Calculate the cark current.

        This function calculates the dark current for each SPARC4 CCD. This is
        an abstract function that is extended in the child classes.

        Returns
        -------
        dakr current: float
            Dark current of the respective SPARC4 CCD.

        """
        dark_current = 0
        return dark_current

    def calculate_read_noise(self, ccd_operation_mode):
        """Calculate the read noise the CCD.

        The calculation is performed by providing the CCD operation mode to
        the ReadNoiseCalc package
        """
        RN = Read_Noise_Calculation(ccd_operation_mode,
                                    directory=f'Channel {self._CHANNEL_ID}')
        self.read_noise = RN.calculate_read_noise()

        return self.read_noise


class Concrete_Channel_1(Abstract_Channel_Creator):
    """Concreat Channel Creator Class 1.

    This class calculates the star and/or the sky flux as a function of the
    instrumental response of the SPARC4 Channel 1.
    """

    _CHANNEL_ID = 1
    _SERIAL_NUMBER = 9914

    def _factory_method(self):
        pass

    def calculate_dark_current(self):
        """Calculate the dark current.

        This function extends the function of the Abstract Channel Creator
        class. Here, the dark current in e-/AUD for the Channel 1 is
        calculated.


        Returns
        -------
        dark_ current: float
            Dark current in e-/ADU for the CCD of the Channel 1 of the SPARC4
            instrument.
        """
        T = self.ccd_temp
        self.dark_current = 24.66*np.exp(0.0015*T**2+0.29*T)
        return self.dark_current


class Concrete_Channel_2(Abstract_Channel_Creator):
    """Concreat Channel Creator Class 2.

    This class calculates the star and/or the sky flux as a function of the
    instrumental response of the SPARC4 Channel 2.
    """

    _CHANNEL_ID = 2
    _SERIAL_NUMBER = 9915

    def _factory_method(self):
        pass

    def calculate_dark_current(self):
        """Calculate the dark current.

        This function extends the function of the Abstract Channel Creator
        class. Here, the dark current in e-/AUD for the Channel 2 is
        calculated.


        Returns
        -------
        dark_ current: float
            Dark current in e-/ADU for the CCD of the Channel 1 of the SPARC4
            instrument.
        """
        T = self.ccd_temp
        self.dark_current = 35.26*np.exp(0.0019*T**2+0.31*T)
        return self.dark_current


class Concrete_Channel_3(Abstract_Channel_Creator):
    """Concreat Channel Creator Class 3.

    This class calculates the star and/or the sky flux as a function of the
    instrumental response of the SPARC4 Channel 3.
    """

    _CHANNEL_ID = 3
    _SERIAL_NUMBER = 9916

    def _factory_method(self):
        pass

    def calculate_dark_current(self):
        """Calculate the dark current.

        This function extends the function of the Abstract Channel Creator
        class. Here, the dark current in e-/AUD for the Channel 3 is
        calculated.


        Returns
        -------
        dark_ current: float
            Dark current in e-/ADU for the CCD of the Channel 1 of the SPARC4
            instrument.
        """
        T = self.ccd_temp
        self.dark_current = 9.67*np.exp(0.0012*T**2+0.25*T)
        return self.dark_current


class Concrete_Channel_4(Abstract_Channel_Creator):
    """Concreat Channel Creator Class 4.

    This class calculates the star and/or the sky flux as a function of the
    instrumental response of the SPARC4 Channel 4.
    """

    _CHANNEL_ID = 4
    _SERIAL_NUMBER = 9917

    def _factory_method(self):
        pass

    def calculate_dark_current(self):
        """Calculate the dark current.

        This function extends the function of the Abstract Channel Creator
        class. Here, the dark current in e-/AUD for the Channel 4 is
        calculated.


        Returns
        -------
        dark_ current: float
            Dark current in e-/ADU for the CCD of the Channel 1 of the SPARC4
            instrument.
        """
        T = self.ccd_temp
        self.dark_current = 5.92*np.exp(0.0005*T**2+0.18*T)
        return self.dark_current
