#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .aces_it import ACES_RICD
from .aces import (
    ACES_2065_1_COLOURSPACE,
    ACES_CC_COLOURSPACE,
    ACES_CG_COLOURSPACE,
    ACES_PROXY_COLOURSPACE)
from .adobe_rgb_1998 import ADOBE_RGB_1998_COLOURSPACE
from .adobe_wide_gamut_rgb import ADOBE_WIDE_GAMUT_RGB_COLOURSPACE
from .alexa_wide_gamut_rgb import ALEXA_WIDE_GAMUT_RGB_COLOURSPACE
from .apple_rgb import APPLE_RGB_COLOURSPACE
from .best_rgb import BEST_RGB_COLOURSPACE
from .beta_rgb import BETA_RGB_COLOURSPACE
from .cie_rgb import CIE_RGB_COLOURSPACE
from .cinema_gamut import CINEMA_GAMUT_COLOURSPACE
from .color_match_rgb import COLOR_MATCH_RGB_COLOURSPACE
from .dci_p3 import DCI_P3_COLOURSPACE, DCI_P3_P_COLOURSPACE
from .don_rgb_4 import DON_RGB_4_COLOURSPACE
from .eci_rgb_v2 import ECI_RGB_V2_COLOURSPACE
from .ekta_space_ps5 import EKTA_SPACE_PS_5_COLOURSPACE
from .max_rgb import MAX_RGB_COLOURSPACE
from .ntsc_rgb import NTSC_RGB_COLOURSPACE
from .pal_secam_rgb import PAL_SECAM_RGB_COLOURSPACE
from .prophoto_rgb import PROPHOTO_RGB_COLOURSPACE
from .rec_709 import REC_709_COLOURSPACE
from .rec_2020 import REC_2020_COLOURSPACE
from .russell_rgb import RUSSELL_RGB_COLOURSPACE
from .s_gamut import (S_GAMUT_COLOURSPACE,
                      S_GAMUT3_COLOURSPACE,
                      S_GAMUT3_CINE_COLOURSPACE)
from .smptec_rgb import SMPTE_C_RGB_COLOURSPACE
from .srgb import sRGB_COLOURSPACE
from .xtreme_rgb import XTREME_RGB_COLOURSPACE

from .pointer_gamut import (
    POINTER_GAMUT_ILLUMINANT,
    POINTER_GAMUT_DATA,
    POINTER_GAMUT_BOUNDARIES)

from colour.utilities import CaseInsensitiveMapping

RGB_COLOURSPACES = CaseInsensitiveMapping(
    {ACES_2065_1_COLOURSPACE.name: ACES_2065_1_COLOURSPACE,
     ACES_CC_COLOURSPACE.name: ACES_CC_COLOURSPACE,
     ACES_PROXY_COLOURSPACE.name: ACES_PROXY_COLOURSPACE,
     ACES_CG_COLOURSPACE.name: ACES_CG_COLOURSPACE,
     ADOBE_RGB_1998_COLOURSPACE.name: ADOBE_RGB_1998_COLOURSPACE,
     ADOBE_WIDE_GAMUT_RGB_COLOURSPACE.name: ADOBE_WIDE_GAMUT_RGB_COLOURSPACE,
     ALEXA_WIDE_GAMUT_RGB_COLOURSPACE.name: ALEXA_WIDE_GAMUT_RGB_COLOURSPACE,
     APPLE_RGB_COLOURSPACE.name: APPLE_RGB_COLOURSPACE,
     BEST_RGB_COLOURSPACE.name: BEST_RGB_COLOURSPACE,
     BETA_RGB_COLOURSPACE.name: BETA_RGB_COLOURSPACE,
     CIE_RGB_COLOURSPACE.name: CIE_RGB_COLOURSPACE,
     CINEMA_GAMUT_COLOURSPACE.name: CINEMA_GAMUT_COLOURSPACE,
     COLOR_MATCH_RGB_COLOURSPACE.name: COLOR_MATCH_RGB_COLOURSPACE,
     DCI_P3_COLOURSPACE.name: DCI_P3_COLOURSPACE,
     DCI_P3_P_COLOURSPACE.name: DCI_P3_P_COLOURSPACE,
     DON_RGB_4_COLOURSPACE.name: DON_RGB_4_COLOURSPACE,
     ECI_RGB_V2_COLOURSPACE.name: ECI_RGB_V2_COLOURSPACE,
     EKTA_SPACE_PS_5_COLOURSPACE.name: EKTA_SPACE_PS_5_COLOURSPACE,
     MAX_RGB_COLOURSPACE.name: MAX_RGB_COLOURSPACE,
     NTSC_RGB_COLOURSPACE.name: NTSC_RGB_COLOURSPACE,
     PAL_SECAM_RGB_COLOURSPACE.name: PAL_SECAM_RGB_COLOURSPACE,
     PROPHOTO_RGB_COLOURSPACE.name: PROPHOTO_RGB_COLOURSPACE,
     REC_709_COLOURSPACE.name: REC_709_COLOURSPACE,
     REC_2020_COLOURSPACE.name: REC_2020_COLOURSPACE,
     RUSSELL_RGB_COLOURSPACE.name: RUSSELL_RGB_COLOURSPACE,
     S_GAMUT_COLOURSPACE.name: S_GAMUT_COLOURSPACE,
     S_GAMUT3_COLOURSPACE.name: S_GAMUT3_COLOURSPACE,
     S_GAMUT3_CINE_COLOURSPACE.name: S_GAMUT3_CINE_COLOURSPACE,
     SMPTE_C_RGB_COLOURSPACE.name: SMPTE_C_RGB_COLOURSPACE,
     sRGB_COLOURSPACE.name: sRGB_COLOURSPACE,
     XTREME_RGB_COLOURSPACE.name: XTREME_RGB_COLOURSPACE})
"""
Aggregated *RGB* colourspaces.

RGB_COLOURSPACES : CaseInsensitiveMapping

Aliases:

-   'aces': ACES_2065_1_COLOURSPACE.name
-   'adobe1998': ADOBE_RGB_1998_COLOURSPACE.name
-   'prophoto': PROPHOTO_RGB_COLOURSPACE.name
"""
RGB_COLOURSPACES['aces'] = (
    RGB_COLOURSPACES[ACES_2065_1_COLOURSPACE.name])
RGB_COLOURSPACES['adobe1998'] = (
    RGB_COLOURSPACES[ADOBE_RGB_1998_COLOURSPACE.name])
RGB_COLOURSPACES['prophoto'] = (
    RGB_COLOURSPACES[PROPHOTO_RGB_COLOURSPACE.name])

__all__ = ['ACES_RICD']
__all__ += ['RGB_COLOURSPACES']
__all__ += ['ACES_2065_1_COLOURSPACE',
            'ACES_CC_COLOURSPACE',
            'ACES_PROXY_COLOURSPACE',
            'ACES_CG_COLOURSPACE',
            'ADOBE_RGB_1998_COLOURSPACE',
            'ADOBE_WIDE_GAMUT_RGB_COLOURSPACE',
            'ALEXA_WIDE_GAMUT_RGB_COLOURSPACE',
            'APPLE_RGB_COLOURSPACE',
            'BEST_RGB_COLOURSPACE',
            'BETA_RGB_COLOURSPACE',
            'CIE_RGB_COLOURSPACE',
            'CINEMA_GAMUT_COLOURSPACE',
            'COLOR_MATCH_RGB_COLOURSPACE',
            'DCI_P3_COLOURSPACE',
            'DCI_P3_P_COLOURSPACE',
            'DON_RGB_4_COLOURSPACE',
            'ECI_RGB_V2_COLOURSPACE',
            'EKTA_SPACE_PS_5_COLOURSPACE',
            'MAX_RGB_COLOURSPACE',
            'NTSC_RGB_COLOURSPACE',
            'PAL_SECAM_RGB_COLOURSPACE',
            'PROPHOTO_RGB_COLOURSPACE',
            'REC_709_COLOURSPACE',
            'REC_2020_COLOURSPACE',
            'RUSSELL_RGB_COLOURSPACE',
            'S_GAMUT_COLOURSPACE',
            'S_GAMUT3_COLOURSPACE',
            'S_GAMUT3_CINE_COLOURSPACE',
            'SMPTE_C_RGB_COLOURSPACE',
            'sRGB_COLOURSPACE',
            'XTREME_RGB_COLOURSPACE']
__all__ += ['POINTER_GAMUT_ILLUMINANT',
            'POINTER_GAMUT_DATA',
            'POINTER_GAMUT_BOUNDARIES']
