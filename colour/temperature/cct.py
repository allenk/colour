#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Correlated Colour Temperature :math:`T_{cp}`
============================================

Defines correlated colour temperature :math:`T_{cp}` computations objects:

-   :func:`uv_to_CCT_ohno2013`: Correlated colour temperature :math:`T_{cp}`
    and :math:`\Delta_{uv}` computation of given *CIE UCS* colourspace *uv*
    chromaticity coordinates using *Yoshi Ohno (2013)* method.
-   :func:`CCT_to_uv_ohno2013`: *CIE UCS* colourspace *uv* chromaticity
    coordinates computation of given correlated colour temperature
    :math:`T_{cp}`, :math:`\Delta_{uv}` using *Yoshi Ohno (2013)* method.
-   :func:`uv_to_CCT_robertson1968`: Correlated colour temperature
    :math:`T_{cp}` and :math:`\Delta_{uv}` computation of given *CIE UCS*
    colourspace *uv* chromaticity coordinates using *Robertson (1968)* method.
-   :func:`CCT_to_uv_robertson1968`: *CIE UCS* colourspace *uv* chromaticity
    coordinates computation of given correlated colour temperature
    :math:`T_{cp}` and :math:`\Delta_{uv}` using *Robertson (1968)* method.
-   :func:`xy_to_CCT_mccamy1992`: Correlated colour temperature :math:`T_{cp}`
    computation of given *CIE XYZ* colourspace *xy* chromaticity coordinates
    using *McCamy (1992)* method.
-   :func:`xy_to_CCT_hernandez1999`: Correlated colour temperature
    :math:`T_{cp}` computation of given *CIE XYZ* colourspace *xy* chromaticity
    coordinates using *Hernandez-Andres, Lee & Romero (1999)* method.
-   :func:`CCT_to_xy_kang2002`: *CIE XYZ* colourspace *xy* chromaticity
    coordinates computation of given correlated colour temperature
    :math:`T_{cp}` using *Kang, Moon, Hong, Lee, Cho and Kim (2002)* method.
-   :func:`CCT_to_xy_illuminant_D`: *CIE XYZ* colourspace *xy* chromaticity
    coordinates computation of *CIE Illuminant D Series* from given correlated
    colour temperature :math:`T_{cp}` of that *CIE Illuminant D Series*.

References
----------
.. [1]  http://en.wikipedia.org/wiki/Color_temperature
"""

from __future__ import unicode_literals

import math
import numpy as np
from collections import namedtuple

from colour.colorimetry import (
    STANDARD_OBSERVERS_CMFS,
    blackbody_spectral_power_distribution,
    spectral_to_XYZ)
from colour.models import UCS_to_uv, XYZ_to_UCS
from colour.utilities import warning

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2013 - 2014 - Colour Developers"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Colour Developers"
__email__ = "colour-science@googlegroups.com"
__status__ = "Production"

__all__ = ["PLANCKIAN_TABLE_TUVD",
           "CCT_MINIMAL",
           "CCT_MAXIMAL",
           "CCT_SAMPLES",
           "CCT_CALCULATION_ITERATIONS",
           "ROBERTSON_ISOTEMPERATURE_LINES_DATA",
           "ROBERTSON_ISOTEMPERATURE_LINES_RUVT",
           "ROBERTSON_ISOTEMPERATURE_LINES",
           "get_planckian_table",
           "get_planckian_table_minimal_distance_index",
           "uv_to_CCT_ohno2013",
           "CCT_to_uv_ohno2013",
           "uv_to_CCT_robertson1968",
           "CCT_to_uv_robertson1968",
           "UV_TO_CCT_METHODS",
           "uv_to_CCT",
           "CCT_TO_UV_METHODS",
           "CCT_to_uv",
           "xy_to_CCT_mccamy1992",
           "xy_to_CCT_hernandez1999",
           "CCT_to_xy_kang2002",
           "CCT_to_xy_illuminant_D",
           "XY_TO_CCT_METHODS",
           "xy_to_CCT",
           "CCT_TO_XY_METHODS",
           "CCT_to_xy"]

PLANCKIAN_TABLE_TUVD = namedtuple("PlanckianTable_Tuvdi",
                                  ("Ti", "ui", "vi", "di"))

CCT_MINIMAL = 1000
CCT_MAXIMAL = 100000
CCT_SAMPLES = 10
CCT_CALCULATION_ITERATIONS = 6

ROBERTSON_ISOTEMPERATURE_LINES_DATA = (
    (0, 0.18006, 0.26352, -0.24341),
    (10, 0.18066, 0.26589, -0.25479),
    (20, 0.18133, 0.26846, -0.26876),
    (30, 0.18208, 0.27119, -0.28539),
    (40, 0.18293, 0.27407, -0.30470),
    (50, 0.18388, 0.27709, -0.32675),
    (60, 0.18494, 0.28021, -0.35156),
    (70, 0.18611, 0.28342, -0.37915),
    (80, 0.18740, 0.28668, -0.40955),
    (90, 0.18880, 0.28997, -0.44278),
    (100, 0.19032, 0.29326, -0.47888),
    (125, 0.19462, 0.30141, -0.58204),
    (150, 0.19962, 0.30921, -0.70471),
    (175, 0.20525, 0.31647, -0.84901),
    (200, 0.21142, 0.32312, -1.0182),
    (225, 0.21807, 0.32909, -1.2168),
    (250, 0.22511, 0.33439, -1.4512),
    (275, 0.23247, 0.33904, -1.7298),
    (300, 0.24010, 0.34308, -2.0637),
    (325, 0.24792, 0.34655, -2.4681),  # 0.24702 ---> 0.24792 Bruce Lindbloom
    (350, 0.25591, 0.34951, -2.9641),
    (375, 0.26400, 0.35200, -3.5814),
    (400, 0.27218, 0.35407, -4.3633),
    (425, 0.28039, 0.35577, -5.3762),
    (450, 0.28863, 0.35714, -6.7262),
    (475, 0.29685, 0.35823, -8.5955),
    (500, 0.30505, 0.35907, -11.324),
    (525, 0.31320, 0.35968, -15.628),
    (550, 0.32129, 0.36011, -23.325),
    (575, 0.32931, 0.36038, -40.770),
    (600, 0.33724, 0.36051, -116.45))
"""
*Robertson* iso-temperature lines.

ROBERTSON_ISOTEMPERATURE_LINES_DATA : tuple
    (Reciprocal Megakelvin,
    CIE 1960 Chromaticity Coordinate *u*,
    CIE 1960 Chromaticity Coordinate *v*,
    Slope)

Notes
-----
-   A correction has been done by *Bruce Lindbloom* for *325* Megakelvin
    temperature: 0.24702 ---> 0.24792

References
----------
.. [1]  **Wyszecki & Stiles**,
        *Color Science - Concepts and Methods Data and Formulae -
        Second Edition*,
        Wiley Classics Library Edition, published 2000, ISBN-10: 0-471-39918-3,
        Page 228.
"""

ROBERTSON_ISOTEMPERATURE_LINES_RUVT = namedtuple(
    "WyszeckiRobertson_ruvt", ("r", "u", "v", "t"))

ROBERTSON_ISOTEMPERATURE_LINES = [
    ROBERTSON_ISOTEMPERATURE_LINES_RUVT(*x)
    for x in ROBERTSON_ISOTEMPERATURE_LINES_DATA]


def get_planckian_table(uv, cmfs, start, end, count):
    """
    Returns a planckian table from given *CIE UCS* colourspace *uv*
    chromaticity coordinates, colour matching functions and temperature range
    using *Yoshi Ohno (2013)* method.

    Parameters
    ----------
    uv : array_like
        *uv* chromaticity coordinates.
    cmfs : XYZ_ColourMatchingFunctions
        Standard observer colour matching functions.
    start : float
        Temperature range start in kelvins.
    end : float
        Temperature range end in kelvins.
    count : int
        Temperatures count in the planckian table.

    Returns
    -------
    list
        Planckian table.

    Examples
    --------
    >>> import pprint
    >>> cmfs = colour.STANDARD_OBSERVERS_CMFS.get("CIE 1931 2 Degree Standard Observer")
    >>> pprint.pprint(colour.temperature.cct.get_planckian_table((0.1978, 0.3122), cmfs, 1000, 1010, 10))
    [PlanckianTableTuvdi(Ti=1000.0, ui=0.44800695592713469, vi=0.35462532232761207, di=0.2537783063402483),
     PlanckianTableTuvdi(Ti=1001.1111111111111, ui=0.44774688726773565, vi=0.3546478595072966, di=0.25352567371290297),
     PlanckianTableTuvdi(Ti=1002.2222222222222, ui=0.44748712505363253, vi=0.35467035108531186, di=0.2532733526031864),
     PlanckianTableTuvdi(Ti=1003.3333333333334, ui=0.44722766912561784, vi=0.35469279704978462, di=0.2530213428281355),
     PlanckianTableTuvdi(Ti=1004.4444444444445, ui=0.44696851932239223, vi=0.35471519738915419, di=0.2527696442026852),
     PlanckianTableTuvdi(Ti=1005.5555555555555, ui=0.44670967548058027, vi=0.35473755209217106, di=0.25251825653968457),
     PlanckianTableTuvdi(Ti=1006.6666666666666, ui=0.4464511374347529, vi=0.35475986114789521, di=0.25226717964991896),
     PlanckianTableTuvdi(Ti=1007.7777777777778, ui=0.44619290501744918, vi=0.3547821245456938, di=0.2520164133421324),
     PlanckianTableTuvdi(Ti=1008.8888888888889, ui=0.44593497805919297, vi=0.35480434227524021, di=0.251765957423044),
     PlanckianTableTuvdi(Ti=1010.0, ui=0.4456773563885123, vi=0.35482651432651208, di=0.251515811697368)]
    """

    ux, vx = uv

    planckian_table = []
    for Ti in np.linspace(start, end, count):
        spd = blackbody_spectral_power_distribution(Ti, *cmfs.shape)
        XYZ = spectral_to_XYZ(spd, cmfs)
        XYZ *= 1. / np.max(XYZ)
        UVW = XYZ_to_UCS(XYZ)
        ui, vi = UCS_to_uv(UVW)
        di = math.sqrt((ux - ui) ** 2 + (vx - vi) ** 2)
        planckian_table.append(PLANCKIAN_TABLE_TUVD(Ti, ui, vi, di))

    return planckian_table


def get_planckian_table_minimal_distance_index(planckian_table):
    """
    Returns the shortest distance index in given planckian table using
    *Yoshi Ohno (2013)* method.

    Parameters
    ----------
    planckian_table : list
        Planckian table.

    Returns
    -------
    int
        Shortest distance index.

    Examples
    --------
    >>> cmfs = colour.STANDARD_OBSERVERS_CMFS.get("CIE 1931 2 Degree Standard Observer")
    >>> colour.temperature.get_planckian_table_minimal_distance_index(get_planckian_table((0.1978, 0.3122), cmfs, 1000, 1010, 10)))
    9
    """

    distances = [x.di for x in planckian_table]
    return distances.index(min(distances))


def uv_to_CCT_ohno2013(uv,
                       cmfs=STANDARD_OBSERVERS_CMFS.get(
                           "CIE 1931 2 Degree Standard Observer"),
                       start=CCT_MINIMAL,
                       end=CCT_MAXIMAL,
                       count=CCT_SAMPLES,
                       iterations=CCT_CALCULATION_ITERATIONS):
    """
    Returns the correlated colour temperature :math:`T_{cp}` and
    :math:`\Delta_{uv}` from given *CIE UCS* colourspace *uv* chromaticity
    coordinates, colour matching functions and temperature range using
    *Yoshi Ohno (2013)* method.

    The iterations parameter defines the calculations precision: The higher its
    value, the more planckian tables will be generated through cascade
    expansion in order to converge to the exact solution.

    Parameters
    ----------
    uv : array_like
        *CIE UCS* colourspace *uv* chromaticity coordinates.
    cmfs : XYZ_ColourMatchingFunctions, optional
        Standard observer colour matching functions.
    start : float, optional
        Temperature range start in kelvins.
    end : float, optional
        Temperature range end in kelvins.
    count : int, optional
        Temperatures count in the planckian tables.
    iterations : int, optional
        Number of planckian tables to generate.

    Returns
    -------
    tuple
        Correlated colour temperature :math:`T_{cp}`, :math:`\Delta_{uv}`.

    References
    ----------
    .. [2]  **Yoshi Ohno**, `Practical Use and Calculation of CCT and Duv
            <http://dx.doi.org/10.1080/15502724.2014.839020>`_

    Examples
    --------
    >>> cmfs = colour.STANDARD_OBSERVERS_CMFS.get("CIE 1931 2 Degree Standard Observer")
    >>> colour.uv_to_CCT_ohno2013((0.1978, 0.3122), cmfs)
    (6507.4342201047066, 0.003223690901512735)
    """

    # Ensuring we do at least one iteration to initialise variables.
    if iterations <= 0:
        iterations = 1

    # Planckian table creation through cascade expansion.
    for i in range(iterations):
        planckian_table = get_planckian_table(uv, cmfs, start, end, count)
        index = get_planckian_table_minimal_distance_index(planckian_table)
        if index == 0:
            warning("Minimal distance index is on lowest planckian table bound, \
unpredictable results may occur!")
            index += 1
        elif index == len(planckian_table) - 1:
            warning("Minimal distance index is on highest planckian table bound, \
unpredictable results may occur!")
            index -= 1

        start = planckian_table[index - 1].Ti
        end = planckian_table[index + 1].Ti

    ux, vx = uv

    Tuvdip, Tuvdi, Tuvdin = (planckian_table[index - 1],
                             planckian_table[index],
                             planckian_table[index + 1])
    Tip, uip, vip, dip = Tuvdip.Ti, Tuvdip.ui, Tuvdip.vi, Tuvdip.di
    Ti, ui, vi, di = Tuvdi.Ti, Tuvdi.ui, Tuvdi.vi, Tuvdi.di
    Tin, uin, vin, din = Tuvdin.Ti, Tuvdin.ui, Tuvdin.vi, Tuvdin.di

    # Triangular solution.
    l = math.sqrt((uin - uip) ** 2 + (vin - vip) ** 2)
    x = (dip ** 2 - din ** 2 + l ** 2) / (2 * l)
    T = Tip + (Tin - Tip) * (x / l)

    vtx = vip + (vin - vip) * (x / l)
    sign = 1. if vx - vtx >= 0. else -1.
    Duv = (dip ** 2 - x ** 2) ** (1. / 2.) * sign

    # Parabolic solution.
    if Duv < 0.002:
        X = (Tin - Ti) * (Tip - Tin) * (Ti - Tip)
        a = (Tip * (din - di) + Ti * (dip - din) + Tin * (di - dip)) * X ** -1
        b = (-(Tip ** 2 * (din - di) + Ti ** 2 * (dip - din) + Tin ** 2 *
               (di - dip)) * X ** -1)
        c = (-(dip * (Tin - Ti) * Ti * Tin + di * (Tip - Tin) * Tip * Tin
               + din * (Ti - Tip) * Tip * Ti) * X ** -1)

        T = -b / (2. * a)

        Duv = sign * (a * T ** 2 + b * T + c)

    return T, Duv


def CCT_to_uv_ohno2013(CCT,
                       Duv=0.,
                       cmfs=STANDARD_OBSERVERS_CMFS.get(
                           "CIE 1931 2 Degree Standard Observer")):
    """
    Returns the *CIE UCS* colourspace *uv* chromaticity coordinates from given
    correlated colour temperature :math:`T_{cp}`, :math:`\Delta_{uv}` and
    colour matching functions using *Yoshi Ohno (2013)* method.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.
    Duv : float, optional
        :math:`\Delta_{uv}`.
    cmfs : XYZ_ColourMatchingFunctions, optional
        Standard observer colour matching functions.

    Returns
    -------
    tuple
        *CIE UCS* colourspace *uv* chromaticity coordinates.

    References
    ----------
    .. [3]  **Yoshi Ohno**, `Practical Use and Calculation of CCT and Duv
            <http://dx.doi.org/10.1080/15502724.2014.839020>`_

    Examples
    --------
    >>> cmfs = colour.STANDARD_OBSERVERS_CMFS.get("CIE 1931 2 Degree Standard Observer")
    >>> colour.CCT_to_uv_ohno2013(6507.4342201047066, 0.003223690901512735, cmfs)
    (0.19779977151790701, 0.31219970605380082)
    """

    delta = 0.01

    spd = blackbody_spectral_power_distribution(CCT, *cmfs.shape)
    XYZ = spectral_to_XYZ(spd, cmfs)
    XYZ *= 1. / np.max(XYZ)
    UVW = XYZ_to_UCS(XYZ)
    u0, v0 = UCS_to_uv(UVW)

    if Duv == 0.:
        return u0, v0
    else:
        spd = blackbody_spectral_power_distribution(CCT + delta, *cmfs.shape)
        XYZ = spectral_to_XYZ(spd, cmfs)
        XYZ *= 1. / np.max(XYZ)
        UVW = XYZ_to_UCS(XYZ)
        u1, v1 = UCS_to_uv(UVW)

        du = u0 - u1
        dv = v0 - v1

        u = u0 - Duv * (dv / math.sqrt(du ** 2 + dv ** 2))
        v = v0 + Duv * (du / math.sqrt(du ** 2 + dv ** 2))

        return u, v


def uv_to_CCT_robertson1968(uv):
    """
    Returns the correlated colour temperature :math:`T_{cp}` and
    :math:`\Delta_{uv}` from given *CIE UCS* colourspace *uv* chromaticity
    coordinates using *Robertson (1968)* method.

    Parameters
    ----------
    uv : array_like
        *CIE UCS* colourspace *uv* chromaticity coordinates.

    Returns
    -------
    tuple
        Correlated colour temperature :math:`T_{cp}`, :math:`\Delta_{uv}`.

    References
    ----------
    .. [4]  **Wyszecki & Stiles**,
            *Color Science - Concepts and Methods Data and Formulae -
            Second Edition*,
            Wiley Classics Library Edition, published 2000,
            ISBN-10: 0-471-39918-3,
            Page 227.
    .. [5]  *Adobe DNG SDK 1.3.0.0*:
            *dng_sdk_1_3/dng_sdk/source/dng_temperature.cpp*:
            *dng_temperature::Set_xy_coord*.

    Examples
    --------
    >>> colour.uv_to_CCT_robertson1968((0.19374137599822966, 0.31522104394059397))
    (6500.016287949829, 0.008333328983860189)
    """

    u, v = uv

    last_dt = last_dv = last_du = 0.0

    for i in range(1, 31):
        wr_ruvt = ROBERTSON_ISOTEMPERATURE_LINES[i]
        wr_ruvt_previous = ROBERTSON_ISOTEMPERATURE_LINES[i - 1]

        du = 1.0
        dv = wr_ruvt.t

        len = math.sqrt(1. + dv * dv)

        du /= len
        dv /= len

        uu = u - wr_ruvt.u
        vv = v - wr_ruvt.v

        dt = -uu * dv + vv * du

        if dt <= 0. or i == 30:
            if dt > 0.0:
                dt = 0.0

            dt = -dt

            if i == 1:
                f = 0.0
            else:
                f = dt / (last_dt + dt)

            T = 1.0e6 / (wr_ruvt_previous.r * f + wr_ruvt.r * (1. - f))

            uu = u - (wr_ruvt_previous.u * f + wr_ruvt.u * (1. - f))
            vv = v - (wr_ruvt_previous.v * f + wr_ruvt.v * (1. - f))

            du = du * (1. - f) + last_du * f
            dv = dv * (1. - f) + last_dv * f

            len = math.sqrt(du * du + dv * dv)

            du /= len
            dv /= len

            Duv = uu * du + vv * dv

            break

        last_dt = dt
        last_du = du
        last_dv = dv

    return T, -Duv


def CCT_to_uv_robertson1968(CCT, Duv=0.):
    """
    Returns the *CIE UCS* colourspace *uv* chromaticity coordinates from given
    correlated colour temperature :math:`T_{cp}` and :math:`\Delta_{uv}` using
    *Robertson (1968)* method.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.
    Duv : float
        :math:`\Delta_{uv}`.

    Returns
    -------
    tuple
        *CIE UCS* colourspace *uv* chromaticity coordinates.

    References
    ----------
    .. [6]  **Wyszecki & Stiles**,
            *Color Science - Concepts and Methods Data and Formulae -
            Second Edition*,
            Wiley Classics Library Edition, published 2000,
            ISBN-10: 0-471-39918-3,
            Page 227.
    .. [7]  *Adobe DNG SDK 1.3.0.0*:
            *dng_sdk_1_3/dng_sdk/source/dng_temperature.cpp*:
            *dng_temperature::Get_xy_coord*.
    Examples
    --------
    >>> colour.CCT_to_uv_robertson1968(6500.0081378199056, 0.0083333312442250979)
    (0.19374137599822966, 0.31522104394059397)
    """

    r = 1.0e6 / CCT

    for i in range(30):
        wr_ruvt = ROBERTSON_ISOTEMPERATURE_LINES[i]
        wr_ruvt_next = ROBERTSON_ISOTEMPERATURE_LINES[i + 1]

        if r < wr_ruvt_next.r or i == 29:
            f = (wr_ruvt_next.r - r) / (wr_ruvt_next.r - wr_ruvt.r)

            u = wr_ruvt.u * f + wr_ruvt_next.u * (1. - f)
            v = wr_ruvt.v * f + wr_ruvt_next.v * (1. - f)

            uu1 = uu2 = 1.0
            vv1, vv2 = wr_ruvt.t, wr_ruvt_next.t

            len1, len2 = math.sqrt(1. + vv1 * vv1), math.sqrt(1. + vv2 * vv2)

            uu1 /= len1
            vv1 /= len1

            uu2 /= len2
            vv2 /= len2

            uu3 = uu1 * f + uu2 * (1. - f)
            vv3 = vv1 * f + vv2 * (1. - f)

            len3 = math.sqrt(uu3 * uu3 + vv3 * vv3)

            uu3 /= len3
            vv3 /= len3

            u += uu3 * -Duv
            v += vv3 * -Duv

            return u, v


UV_TO_CCT_METHODS = {"Ohno 2013": uv_to_CCT_ohno2013,
                     "Robertson 1968": uv_to_CCT_robertson1968}
"""
Supported *CIE UCS* colourspace *uv* chromaticity coordinates to correlated
colour temperature :math:`T_{cp}` computation methods.

UV_TO_CCT_METHODS : dict
    ("Ohno 2013", "Robertson 1968")
"""

def uv_to_CCT(uv, method="Ohno 2013", **kwargs):
    """
    Returns the correlated colour temperature :math:`T_{cp}` and
    :math:`\Delta_{uv}` from given *CIE UCS* colourspace *uv* chromaticity
    coordinates using given method.

    Parameters
    ----------
    uv : array_like
        *CIE UCS* colourspace *uv* chromaticity coordinates.
    method : unicode
        ("Ohno 2013", "Robertson 1968")
        Computation method.
    \*\*kwargs : \*\*
        Keywords arguments.

    Returns
    -------
    tuple
        Correlated colour temperature :math:`T_{cp}`, :math:`\Delta_{uv}`.
    """

    if method == "Ohno 2013":
        return UV_TO_CCT_METHODS.get(method)(uv, **kwargs)
    else:
        if "cmfs" in kwargs:
            if kwargs.get("cmfs").name != \
                    "CIE 1931 2 Degree Standard Observer":
                raise ValueError("'Robertson (1968)' method is only valid for \
'CIE 1931 2 Degree Standard Observer'!")

        return UV_TO_CCT_METHODS.get(method)(uv)


CCT_TO_UV_METHODS = {"Ohno 2013": CCT_to_uv_ohno2013,
                     "Robertson 1968": CCT_to_uv_robertson1968}
"""
Supported correlated colour temperature :math:`T_{cp}` to *CIE UCS* colourspace
*uv* chromaticity coordinates computation methods.

CCT_TO_UV_METHODS : dict
    ("Ohno 2013", "Robertson 1968")
"""

def CCT_to_uv(CCT, Duv=0., method="Ohno 2013", **kwargs):
    """
    Returns the *CIE UCS* colourspace *uv* chromaticity coordinates from given
    correlated colour temperature :math:`T_{cp}` and :math:`\Delta_{uv}` using
    given method.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.
    Duv : float
        :math:`\Delta_{uv}`.
    method : unicode
        ("Ohno 2013", "Robertson 1968")
        Computation method.
    \*\*kwargs : \*\*
        Keywords arguments.

    Returns
    -------
    tuple
        *CIE UCS* colourspace *uv* chromaticity coordinates.
    """

    if method == "Ohno 2013":
        return CCT_TO_UV_METHODS.get(method)(CCT, Duv, **kwargs)
    else:
        if "cmfs" in kwargs:
            if kwargs.get("cmfs").name != \
                    "CIE 1931 2 Degree Standard Observer":
                raise ValueError("'Robertson (1968)' method is only valid for \
'CIE 1931 2 Degree Standard Observer'!")

        return CCT_TO_UV_METHODS.get(method)(CCT, Duv)


def xy_to_CCT_mccamy1992(xy):
    """
    Returns the correlated colour temperature :math:`T_{cp}` from given
    *CIE XYZ* colourspace *xy* chromaticity coordinates using *McCamy (1992)*
    method.

    Parameters
    ----------
    xy : array_like
        *xy* chromaticity coordinates.

    Returns
    -------
    float
        Correlated colour temperature :math:`T_{cp}`.

    References
    ----------
    .. [8]  http://en.wikipedia.org/wiki/Color_temperature#Approximation
            (Last accessed 28 June 2014)

    Examples
    --------
    >>> colour.xy_to_CCT_mccamy1992((0.31271, 0.32902))
    6504.38938305
    """

    x, y = xy

    n = (x - 0.3320) / (y - 0.1858)
    CCT = -449. * math.pow(n, 3) + 3525 * math.pow(n, 2) - 6823.3 * n + 5520.33

    return CCT


def xy_to_CCT_hernandez1999(xy):
    """
    Returns the correlated colour temperature :math:`T_{cp}` from given
    *CIE XYZ* colourspace *xy* chromaticity coordinates using
    *Hernandez-Andres, Lee & Romero (1999)* method.

    Parameters
    ----------
    xy : array_like
        *xy* chromaticity coordinates.

    Returns
    -------
    float
        Correlated colour temperature :math:`T_{cp}`.

    References
    ----------
    .. [9]  `Calculating correlated color temperatures across the entire gamut
            of daylight and skylight chromaticities
            <http://www.ugr.es/~colorimg/pdfs/ao_1999_5703.pdf>`_

    Examples
    --------
    >>> colour.xy_to_CCT_hernandez1999((0.31271, 0.32902))
    6500.04215334

    """

    x, y = xy

    n = (x - 0.3366) / (y - 0.1735)
    CCT = (-949.86315 +
           6253.80338 * math.exp(-n / 0.92159) +
           28.70599 * math.exp(-n / 0.20039) +
           0.00004 * math.exp(-n / 0.07125))

    if CCT > 50000:
        n = (x - 0.3356) / (y - 0.1691)
        CCT = (36284.48953 +
               0.00228 * math.exp(-n / 0.07861) +
               5.4535e-36 * math.exp(-n / 0.01543))

    return CCT


def CCT_to_xy_kang2002(CCT):
    """
    Returns the *CIE XYZ* colourspace *xy* chromaticity coordinates from given
    correlated colour temperature :math:`T_{cp}` using
    *Kang, Moon, Hong, Lee, Cho and Kim (2002)* method.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.

    Returns
    -------
    tuple
        *xy* chromaticity coordinates.

    References
    ----------
    .. [10] `Design of Advanced Color -
            Temperature Control System for HDTV Applications
            <http://icpr.snu.ac.kr/resource/wop.pdf/J01/2002/041/R06/J012002041R060865.pdf>`_

    Examples
    --------
    >>> colour.CCT_to_xy_kang2002((0.31271, 0.32902))
    (0.3127077520604209, 0.3291128338173629)
    """

    if 1667 <= CCT <= 4000:
        x = (-0.2661239 * 10 ** 9 / CCT ** 3 -
             0.2343589 * 10 ** 6 / CCT ** 2 +
             0.8776956 * 10 ** 3 / CCT +
             0.179910)
    elif 4000 <= CCT <= 25000:
        x = (-3.0258469 * 10 ** 9 / CCT ** 3 +
             2.1070379 * 10 ** 6 / CCT ** 2 +
             0.2226347 * 10 ** 3 / CCT +
             0.24039)
    else:
        raise ValueError(
            "Correlated colour temperature must be in domain [1667, 25000]!")

    if 1667 <= CCT <= 2222:
        y = (-1.1063814 * x ** 3 -
             1.34811020 * x ** 2 +
             2.18555832 * x -
             0.20219683)
    elif 2222 <= CCT <= 4000:
        y = (-0.9549476 * x ** 3 -
             1.37418593 * x ** 2 +
             2.09137015 * x -
             0.16748867)
    elif 4000 <= CCT <= 25000:
        y = (3.0817580 * x ** 3 -
             5.8733867 * x ** 2 +
             3.75112997 * x -
             0.37001483)

    return x, y


def CCT_to_xy_illuminant_D(CCT):
    """
    Converts from the correlated colour temperature :math:`T_{cp}` of a
    *CIE Illuminant D Series* to the chromaticity of that
    *CIE Illuminant D Series*.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.

    Returns
    -------
    tuple
        *xy* chromaticity coordinates.

    References
    ----------
    .. [11] **Wyszecki & Stiles**,
            *Color Science - Concepts and Methods Data and Formulae -
            Second Edition*,
            Wiley Classics Library Edition, published 2000,
            ISBN-10: 0-471-39918-3,
            Page 145.
    """

    if 4000 <= CCT <= 7000:
        x = (-4.607 * 10 ** 9 / CCT ** 3 +
             2.9678 * 10 ** 6 / CCT ** 2 +
             0.09911 * 10 ** 3 / CCT +
             0.244063)
    elif 7000 < CCT <= 25000:
        x = (-2.0064 * 10 ** 9 / CCT ** 3 +
             1.9018 * 10 ** 6 / CCT ** 2 +
             0.24748 * 10 ** 3 / CCT +
             0.23704)
    else:
        raise ValueError(
            "Correlated colour temperature must be in domain [4000, 25000]!")

    y = -3 * x ** 2 + 2.87 * x - 0.275

    return x, y


XY_TO_CCT_METHODS = {"McCamy 1992": xy_to_CCT_mccamy1992,
                     "Hernandez 1999": xy_to_CCT_hernandez1999}
"""
Supported *CIE XYZ* colourspace *xy* chromaticity coordinates to correlated
colour temperature :math:`T_{cp}` computation methods.

XY_TO_CCT_METHODS : dict
    ("McCamy 1992", "Hernandez 1999")
"""

def xy_to_CCT(xy, method="McCamy 1992", **kwargs):
    """
    Returns the correlated colour temperature :math:`T_{cp}` from given
    *CIE XYZ* colourspace *xy* chromaticity coordinates using given method.

    Parameters
    ----------
    xy : array_like
        *xy* chromaticity coordinates.
    method : unicode ("McCamy 1992", "Hernandez 1999")
        Computation method.

    Returns
    -------
    float
        Correlated colour temperature :math:`T_{cp}`.
    """

    return XY_TO_CCT_METHODS.get(method)(xy)


CCT_TO_XY_METHODS = {"Kang 2002": CCT_to_xy_kang2002,
                     "CIE Illuminant D Series": CCT_to_xy_illuminant_D}
"""
Supported correlated colour temperature :math:`T_{cp}` to *CIE XYZ* colourspace
*xy* chromaticity coordinates computation methods.

CCT_TO_XY_METHODS : dict
    ("Kang 2002", "CIE Illuminant D Series")
"""

def CCT_to_xy(CCT, method="Kang 2002"):
    """
    Returns the *CIE XYZ* colourspace *xy* chromaticity coordinates from given
    correlated colour temperature :math:`T_{cp}` using given method.

    Parameters
    ----------
    CCT : float
        Correlated colour temperature :math:`T_{cp}`.
    method : unicode ("Kang 2002", "CIE Illuminant D Series")
        Computation method.

    Returns
    -------
    tuple
        *xy* chromaticity coordinates.
    """

    return CCT_TO_XY_METHODS.get(method)(CCT)