# -*- coding: utf-8 -*-
"""Flux Calculation class tests.

This script tests the operation of the Background Image Class.

Created on Thu Apr 22 13:44:35 2021

@author: denis
"""


from BGI import Background_Image
from CHC import Concrete_Channel_1
import pytest
import numpy as np

dic = {'em_gain': 1, 'binn': 1, 't_exp': 1, 'preamp': 1, 'hss': 1}


@pytest.fixture
def chc1():
    return Concrete_Channel_1(ccd_temp=-70)


@pytest.fixture
def bgi(chc1):
    return Background_Image(chc1, dic, 3)


# ------------------------ Initialize the class --------------------------

def test_CHC(bgi):
    var = 0
    if bgi.CHC:
        var = 1
    assert var == 1


def test_FC(bgi):
    var = 0
    if bgi.FC:
        var = 1
    assert var == 1


def test_TSR(bgi):
    var = 0
    if bgi.TSR:
        var = 1
    assert var == 1


def test_ASR(bgi):
    var = 0
    if bgi.ASR:
        var = 1
    assert var == 1


def test_em_gain(bgi):
    assert bgi.em_gain == 1


def test_bin(bgi):
    assert bgi.binn == 1


def test_t_exp(bgi):
    assert bgi.t_exp == 1


def test_ccd_gain(bgi):
    assert bgi.ccd_gain == 3


# ----------------------- Calculate sky flux -----------------------------

def test_calc_sky_flux(bgi):
    bgi._calculate_sky_flux()
    assert bgi.sky_flux == 100

# ----------------------- Calculate dark current  -------------------------


def test_create_background_image(bgi):
    assert round(bgi.dark_current, 7) == 5.86e-5


# ----------------------- Calculate Background Image -------------------------

# def test_create_background_image(bgi):
#     assert bgi.create_background_image() == []