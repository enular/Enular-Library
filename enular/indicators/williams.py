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

from . import (Indicator, Highest, Lowest, If, UpDay, DownDay, Accum,
               TrueLow, TrueHigh)



class WilliamsR(Indicator):

    """Williams Percent Range (%R) - a momentum oscillator measuring overbought
    and oversold levels ranging from 0 to -100.

    The default period is set to 14, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - WilliamsR(self.data, period=self.params.period)
        - WilliamsR(self.data, period=self.p.period)
        - WilliamsR(self.data, period=14)
        - WilliamsR(self.data)

    Formula:

        - -100 * (highest - close) / (highest - lowest)

    Additional information found at:
    https://www.investopedia.com/terms/w/williamsr.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r
    
    """

    lines = ('percR', )
    params = (('period', 14),
              ('upperband', -20.0),
              ('lowerband', -80.0))

    plotinfo = dict(plotname='Williams R%')
    plotlines = dict(percR=dict(_name='R%', color='navy'))

    def _plotinif(self):
        self.plotinfo.plotyhlines = [self.params.upperband, self.params.lowerband]

    def __init__(self):
        h = Highest(self.data.high, period=self.params.period)
        l = Lowest(self.data.low, period=self.params.period)
        c = self.data.close

        self.lines.percR = -100.0 * (h - c) / (h - l)

        super(WilliamsR, self).__init__()


class WilliamsAD(Indicator):

    """Williams Accumulation Distribution - used when trading price divergence.
    When the price reaches a new high and the indicator fails to exceed its
    previous high, distribution is taking place. When the price reaches a new
    low and the indicator fails to make a new low, accumulation is occurring.

    This indicator takes no parameters other than 'data'. When calling this
    indicator, use:

        - WilliamsAD(self.data)

    Formula:

        - upday = UpDay(data.close)
        - downday = DownDay(data.close)
        - adup = If(upday, data.close - TrueLow(data), 0)
        - addown = If(downday, data.close - TrueHigh(data), 0)
        - AD = Accum(adup + addown)

    Additional information found at:
    https://www.incrediblecharts.com/indicators/williams_accumulation_distribution.php
    https://www.mql5.com/en/code/7064
    
    """

    lines = ('ad', )

    plotlines = dict(ad=dict(_name='AD', color='navy'))

    def __init__(self):
        upday = UpDay(self.data.close)
        downday = DownDay(self.data.close)

        adup = If(upday, self.data.close - TrueLow(self.data), 0.0)
        addown = If(downday, self.data.close - TrueHigh(self.data), 0.0)

        self.lines.ad = Accum(adup + addown)

        super(WilliamsAD, self).__init__()