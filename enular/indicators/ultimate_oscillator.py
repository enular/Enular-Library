#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
############################################################################
#
#                   Enular Technical Analysis Library
#                       Copyright (C) 2022 Enular
#
# Portions of this project contain code derived from, or inspired by 
# Backtrader https://github.com/mementum/backtrader under the GNU General
# Public License (GPL) version 3:
# Copyright (C) 2015-2020 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, SumN, TrueLow, TrueRange



class UltimateOscillator(Indicator):

    """Ultimate Oscillator - measures the price momentum of an asset over
    multiple timeframes. This indicator takes a weighted moving average over
    three timeframes to reduce volatility.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - p1 = 7
        - p2 = 14
        - p3 = 28

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - UltimateOscillator(self.data, p1=self.params.p1)
        - UltimateOscillator(self.data, p1=self.p.p1, p2=self.p.p2)
        - UltimateOscillator(self.data, p1=7, p2=14, p3=28)
        - UltimateOscillator(self.data)

    Formula:

        - buying pressure = bp = data.close - TrueLow
        - tr = TrueRange
        - average7 = SumN(bp, p1) / SumN(tr, p1)
        - average14 = SumN(bp, p2) / SumN(tr, p2)
        - average28 = SumN(bp, p3) / SumN(tr, p3)
        - UO = 100 x [(4 x average7) + (2 x average14) + average28] / (4 + 2 + 1)

    Additional information found at:
    https://www.investopedia.com/terms/u/ultimateoscillator.asp
    https://en.wikipedia.org/wiki/Ultimate_oscillator
    
    """

    lines = ('uo', )
    params = (('p1', 7),
              ('p2', 14),
              ('p3', 28),
              ('upperband', 70.0),
              ('lowerband', 30.0))
    
    plotlines = dict(uo=dict(_name='=', color='navy'))

    def _plotinit(self):
        baseticks = [10.0, 50.0, 90.0]
        hlines = [self.params.upperband, self.params.lowerband]

        # Plot lines at 0 & 100 to make the scale complete + upper/lower/bands
        self.plotinfo.plotyhlines = hlines
        # Plot ticks at "baseticks" + the user specified upper/lower bands
        self.plotinfo.plotyticks = baseticks + hlines

    def __init__(self):
        bp = self.data.close - TrueLow(self.data)
        tr = TrueRange(self.data)

        av7 = SumN(bp, period=self.params.p1) / SumN(tr, period=self.params.p1)
        av14 = SumN(bp, period=self.params.p2) / SumN(tr, period=self.params.p2)
        av28 = SumN(bp, period=self.params.p3) / SumN(tr, period=self.params.p3)

        # Multiply/divide floats outside of formula to reduce line objects
        factor = 100.0 / (4.0 + 2.0 + 1.0)
        uo = (4.0 * factor) * av7 + (2.0 * factor) * av14 + factor * av28
        self.lines.uo = uo

        super(UltimateOscillator, self).__init__()