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

from . import Indicator, Max, Min, MovAv



class TrueHigh(Indicator):

    """True High - records the highest value from either today's high or
    yesterday's close.

    Formula:

        - max(today's high, previous close)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_true_range
    
    """

    lines = ('truehigh', )

    def __init__(self):
        self.lines.truehigh = Max(self.data.high, self.data.close(-1))

        super(TrueHigh, self).__init__()


class TrueLow(Indicator):

    """True Low - records the lowest value from either today's low or
    yesterday's close.

    Formula:

        - min(today's low, previous close)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_true_range
    
    """

    lines = ('truelow', )

    def __init__(self):
        self.lines.truelow = Min(self.data.low, self.data.close(-1))

        super(TrueLow, self).__init__()


class TrueRange(Indicator):

    """True Range - records the price range between the TrueHigh and the
    TrueLow. Takes the previous close into account when calculating the range
    to check if the range yields a larger value than that of the daily range
    (high-low).

    Formula:

        - TR = max(today's high, previous close) - min(today's low, previous close)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_true_range
    
    """

    alias = ('TR', )
    lines = ('tr', )

    def __init__(self):
        self.lines.tr = TrueHigh(self.data) - TrueLow(self.data)

        super(TrueRange, self).__init__()


class AverageTrueRange(Indicator):

    """Average True Range - factoring in gaps in price movement, the ATR
    indicates the degree of price volatility based on the Smoothed Moving
    Average (SMMA). An expanding ATR indicates increased volatility in the
    market with the range of each bar getting larger, whereas a low ATR value
    indicates a series of periods with smaller ranges (quiet days).
    
    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AverageTrueRange(self.data, period=self.params.period)
        - AverageTrueRange(self.data, period=self.p.period)
        - AverageTrueRange(self.data, period=14)
        - AverageTrueRange(self.data)

    Formula:
    
        - SMMA(TrueRange, period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - AverageTrueRange(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_true_range
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/atr
    https://www.investopedia.com/terms/a/atr.asp
    
    """

    alias = ('ATR', )
    lines = ('atr', )
    params = (('period', 14), ('_movav', MovAv.Smoothed))

    plotlines = dict(atr=dict(color='navy'))

    def __init__(self):
        self.lines.atr = self.params._movav(TrueRange(self.data), period=self.params.period)
        
        super(AverageTrueRange, self).__init__()