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

from backtrader.indicator import Indicator
from . import Max, MovAv
from . import DivZeroByZero



class UpDay(Indicator):

    """Up Day - records which days are up, i.e., the close price is higher than
    the previous day (or period).

    Formula:

        - upday = max(close - prev_close, 0)

    Additional information found at:
    https://en.wikipedia.org/wiki/Relative_strength_index
    
    """

    lines = ('upday', )
    params = (('period', 1), )

    def __init__(self):
        self.lines.upday = Max(self.data - self.data(-self.params.period), 0.0)

        super(UpDay, self).__init__()


class DownDay(Indicator):

    """Down Day - records which days are down, i.e., the close price is lower
    than the previous day (or period).

    Formula:

        - downday = max(prev_close - close, 0)

    Additional information found at:
    https://en.wikipedia.org/wiki/Relative_strength_index
    
    """

    lines = ('downday', )
    params = (('period', 1), )

    def __init__(self):
        self.lines.downday = Max(self.data(-self.params.period) - self.data, 0.0)

        super(DownDay, self).__init__()


class UpDayBool(Indicator):

    """Up Day Boolean - records which days are up, i.e., the close price is
    higher than the previous day (or period).

    Formula:

        - upday = close > prev_close

    Additional information found at:
    https://en.wikipedia.org/wiki/Relative_strength_index
    
    """

    lines = ('upday', )
    params = (('period', 1), )

    def __init__(self):
        self.lines.upday = self.data > self.data(-self.params.period)

        super(UpDayBool, self).__init__()


class DownDayBool(Indicator):

    """down Day Boolean - records which days are down, i.e., the close price is
    lower than the previous day (or period).

    Formula:

        - downday = prev_close > close

    Additional information found at:
    https://en.wikipedia.org/wiki/Relative_strength_index
    
    """

    lines = ('downday', )
    params = (('period', 1), )

    def __init__(self):
        self.lines.downday = self.data(-self.params.period) > self.data

        super(DownDayBool, self).__init__()


class RelativeStrengthIndex(Indicator):

    """Relative Strength Index - measures the speed and magnitude of recent
    changes in price to evaluate overvalued and undervalued conditions. This
    is achieved by calculating the ratio of higher closes against lower closes
    that have been smoothed by a moving average, which is then normalised
    between 0 and 100.

    The default period is set to 14, but can be overridden when calling the
    function.

    Requires 1 mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - RelativeStrengthIndex(self.data, period=self.params.period)
        - RelativeStrengthIndex(self.data, period=self.p.period)
        - RelativeStrengthIndex(self.data, period=14)
        - RelativeStrengthIndex(self.data)

    Formula:

        - up = upday(data)
        - down = downday(data)
        - maup = movingaverage(up, period)
        - madown = movingaverage(down, period)
        - rs = maup / madown
        - rsi = 100 - 100 / (1 + rs)

    Notes:

        - Although the standard moving average is the SMMA, this can be
          switched to any other. For example, use WMA by including
          _movav=WMA in the function.
        - RelativeStrengthIndex(self.data, _movav=WMA)
        - 'safediv' (default: False) if this parameter is True the division
          rs = maup / madown will be checked for the special case in which a
          '0 / 0' or 'x / 0' division may occur
        - 'safehigh' (default: 100.0) will be used as the RSI value for the
          'x / 0' case
        - 'safelow' (default: 50.0) will be used as the RSI value for the
          '0 / 0' case

    Additional information found at:
    https://www.investopedia.com/terms/r/rsi.asp
    https://en.wikipedia.org/wiki/Relative_strength_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/RSI
    
    """

    alias = ('RSI', )
    lines = ('rsi', )
    params = (('period', 14),
              ('_movav', MovAv.Smoothed),
              ('upperband', 70.0),
              ('lowerband', 30.0),
              ('safediv', False),
              ('safehigh', 100.0),
              ('safelow', 50.0),
              ('lookback', 1))
    
    plotlines = dict(rsi=dict(color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        plabels += [self.params.lookback] * self.params.notdefault('lookback')
        return plabels

    def _plotinit(self):
        self.plotinfo.plotyhlines = [self.params.upperband, 50, self.params.lowerband]

    def __init__(self):
        upday = UpDay(self.data, period=self.params.lookback)
        downday = DownDay(self.data, period=self.params.lookback)
        maup = self.params._movav(upday, period=self.params.period)
        madown = self.params._movav(downday, period=self.params.period)
        if not self.params.safediv:
            rs = maup / madown
        else:
            highrs = self._rscalc(self.params.safehigh)
            lowrs = self._rscalc(self.params.safelow)
            rs = DivZeroByZero(maup, madown, highrs, lowrs)

        self.lines.rsi = 100.0 - 100.0 / (1.0 + rs)
        super(RelativeStrengthIndex, self).__init__()

    def _rscalc(self, rsi):
        try:
            rs = (-100.0 / (rsi - 100.0)) - 1.0
        except ZeroDivisionError:
            return float('inf')

        return rs


class RSI_Safe(RelativeStrengthIndex):
    
    """
    Subclass of the RSI which changes the default value of the parameter
    'safediv' to 'True'.

    Relative Strength Index - measures the speed and magnitude of recent
    changes in price to evaluate overvalued and undervalued conditions.
    This is achieved by calculating the ratio of higher closes against
    lower closes that have been smoothed by a moving average, which is
    then normalised between 0 and 100.

    The default period is set to 14, but can be overridden when calling
    the function.

    Requires 1 mandatory parameter, 'data,' with an additional optional
    parameter, 'period.' Examples:

        - RSI_Safe(self.data, period=self.params.period)
        - RSI_Safe(self.data, period=self.p.period)
        - RSI_Safe(self.data, period=14)
        - RSI_Safe(self.data)

    Formula:

        - up = upday(data)
        - down = downday(data)
        - maup = movingaverage(up, period)
        - madown = movingaverage(down, period)
        - rs = maup / madown
        - rsi = 100 - 100 / (1 + rs)

    Notes:

        - Although the standard moving average is the SMMA, this can be
          switched to any other. For example, use WMA by including
          _movav=WMA in the function.
        - RSI_Safe(self.data, _movav=WMA)
        - 'safediv' (default: False) if this parameter is True the division
          rs = maup / madown will be checked for the special case in which a
          '0 / 0' or 'x / 0' division may occur
        - 'safehigh' (default: 100.0) will be used as the RSI value for the
          'x / 0' case
        - 'safelow' (default: 50.0) will be used as the RSI value for the
          '0 / 0' case

    Additional information found at:
    https://www.investopedia.com/terms/r/rsi.asp
    https://en.wikipedia.org/wiki/Relative_strength_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/RSI
    
    """
    
    params = (('safediv', True), )