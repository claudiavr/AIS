# -*- coding: utf-8 -*-
"""Test of the Read Noise Calculation Class.

Created on Fri Apr 23 11:59:02 2021

@author: denis
"""

from RNC import Read_Noise_Calculation
import pytest


dic = {'em_mode': 0, 'em_gain': 1, 'binn': 1,
       'preamp': 1, 'hss': 1}


@pytest.fixture
def rnc():
    return Read_Noise_Calculation(dic, 'Channel 1')


# ------------------------ Initialize the class --------------------------

def test_em_mode(rnc):
    assert rnc.em_mode == 0


def test_em_gain(rnc):
    assert rnc.em_gain == 1


def test_binn(rnc):
    assert rnc.binn == 1


def test_preamp(rnc):
    assert rnc.preamp == 1


def test_hss(rnc):
    assert rnc.hss == 1


def test_directory(rnc):
    assert rnc.directory == 'Channel 1'

# -------------------------- Test calculate read noise funtction ------------


@pytest.mark.parametrize(
    'em_mode, em_gain, hss, preamp, binn, read_noise',
    [(0, 1, 0.1, 1, 1, 8.78),
     (0, 1, 0.1, 1, 2, 8.84),
     (0, 1, 0.1, 2, 1, 3.46),
     (0, 1, 0.1, 2, 2, 3.27),
     (0, 1, 1, 1, 1, 6.67),
     (0, 1, 1, 1, 2, 6.94),
     (0, 1, 1, 2, 1, 4.76),
     (0, 1, 1, 2, 2, 4.79),
     (1, 2, 1, 1, 1, 24.64),
     (1, 2, 1, 1, 2, 33.76),
     (1, 2, 1, 2, 1, 12.05),
     (1, 2, 1, 2, 2, 14.55),
     (1, 2, 10, 1, 1, 83.68),
     (1, 2, 10, 1, 2, 82.93),
     (1, 2, 10, 2, 1, 41.71),
     (1, 2, 10, 2, 2, 41.82),
     (1, 2, 20, 1, 1, 160.06),
     (1, 2, 20, 1, 2, 161.98),
     (1, 2, 20, 2, 1, 66.01),
     (1, 2, 20, 2, 2, 72.71),
     (1, 2, 30, 1, 1, 262.01),
     (1, 2, 30, 1, 2, 273.19),
     (1, 2, 30, 2, 1, 169.25),
     (1, 2, 30, 2, 2, 143.59),
     ]
)
def test_calc_read_noise(rnc, em_mode, em_gain, hss, preamp, binn, read_noise):
    rnc.em_mode = em_mode
    rnc.em_gain = em_gain
    rnc.hss = hss
    rnc.preamp = preamp
    rnc.binn = binn
    rn = rnc.calculate_read_noise()
    assert round(rn, 2) == read_noise
