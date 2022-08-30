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

from . import Indicator, MovAv



class TrueStrengthIndex(Indicator):

    """True Strength Index - a technical momentum oscillator used to identify
    trends and reversals.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period1 = 25
        - period2 = 13
        - pchange = 1

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - TrueStrengthIndex(self.data, period1=self.params.period1)
        - TrueStrengthIndex(self.data, period1=self.p.period1, period2=self.p.period2)
        - TrueStrengthIndex(self.data, period1=25, period2=13, pchange=1)
        - TrueStrengthIndex(self.data)

    Formula:

        - price_change = close - close(pchange)
        - sm1_simple = EMA(price_change, period1)
        - sm1_double = EMA(sm1_simple, period2)
        - sm2_simple = EMA(abs(price_change), period1)
        - sm2_double = EMA(sm2_simple, period2)
        - tsi = 100.0 * sm1_double / sm2_double

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - TrueStrengthIndex(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/t/tsi.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:true_strength_index
    
    """

    alias = ('TSI', )
    lines = ('tsi', )
    params = (('period1', 25),
              ('period2', 13),
              ('pchange', 1),
              ('_movav', MovAv.Exponential))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(tsi=dict(_name='=', color='navy'))


    def __init__(self):
        pc = self.data - self.data(-self.params.pchange)

        sm1 = self.params._movav(pc, period=self.params.period1)
        sm12 = self.params._movav(sm1, period=self.params.period2)

        sm2 = self.params._movav(abs(pc), period=self.params.period1)
        sm22 = self.params._movav(sm2, period=self.params.period2)

        self.lines.tsi = 100.0 * (sm12 / sm22)
        
        super(TrueStrengthIndex, self).__init__()