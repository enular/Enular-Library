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

from . import Indicator, CmpEx


class PivotPoint(Indicator):

    """Pivot Point - defines a level of significance by taking into account the
    average of price bar components of the past period of a larger timeframe.
    For example, when operating with days, the values are taken from the past
    month's fixed prices.

    Data must be resampled to use this indicator. For example:

        - data = bt.feeds.datafeed(dataname=x, timeframe=bt.TimeFrame.Days)
        - cerebro.adddata(data)
        - cerebro.resampledata(data, timeframe=bt.TimeFrame.Months)

    In the __init__ method of the strategy:

        - pivotindicator = bt.ind.PivotPoint(self.data1)  # the resampled data

    This indicator will automatically try and plot the non-resampled data. To
    disable this bevaiour, use the following during construction:

        - _autoplot=False

    Notes:

        - The example shows days and months, but any combination of timeframes
          can be used

    Formula:

        - pivot = (h + l + c) / 3  # variants duplicate close or add open
        - support1 = 2.0 * pivot - high
        - support2 = pivot - (high - low)
        - resistance1 = 2.0 * pivot - low
        - resistance2 = pivot + (high - low)

    Additional information found at:
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:pivot_points
    https://en.wikipedia.org/wiki/Pivot_point_(technical_analysis)

    """

    lines = ('p', 's1', 's2', 'r1', 'r2')
    params = (('open', False),  # add opening price to the pivot point
              ('close', False),  # use close twice in the calcs
              ('_autoplot', True))  # attempt to plot on real target data
    
    plotinfo = dict(subplot=False)

    def _plotinit(self):
        # Try to plot to the actual timeframe master
        if self.params._autoplot:
            if hasattr(self.data, 'data'):
                self.plotinfo.plotmaster = self.data.data

    def __init__(self):
        o = self.data.open
        h = self.data.high  # current high
        l = self.data.low  # current low
        c = self.data.close  # current close

        if self.params.close:
            self.lines.p = p = (h + l + 2.0 * c) / 4.0
        elif self.params.open:
            self.lines.p = p = (h + l + c + o) / 4.0
        else:
            self.lines.p = p = (h + l + c) / 3.0

        self.lines.s1 = 2.0 * p - h
        self.lines.r1 = 2.0 * p - l

        self.lines.s2 = p - (h - l)
        self.lines.r2 = p + (h - l)

        super(PivotPoint, self).__init__()  # enable coopertive inheritance

        if self.params._autoplot:
            self.plotinfo.plot = False  # disable own plotting
            self()  # Coupler to follow real object


class FibonacciPivotPoint(Indicator):

    """Fibonacci Pivot Point - defines a level of significance by taking into
    account the average of price bar components of the past period of a larger
    timeframe. For example, when operating with days, the values are taken from
    the past month's fixed prices.

    Fibonacci levels (configurable) are used to define the support/resistance
    levels.

    Data must be resampled to use this indicator. For example:

        - data = bt.feeds.datafeed(dataname=x, timeframe=bt.TimeFrame.Days)
        - cerebro.adddata(data)
        - cerebro.resampledata(data, timeframe=bt.TimeFrame.Months)

    In the __init__ method of the strategy:

        - pivot = bt.ind.FibonacciPivotPoint(self.data1)  # the resampled data

    This indicator will automatically try and plot the non-resampled data. To
    disable this bevaiour, use the following during construction:

        - _autoplot=False

    Notes:

        - The example shows days and months, but any combination of timeframes
          can be used

    Formula:

        - pivot = (h + l + c) / 3  # variants duplicate close or add open
        - support1 = p - level1 * (high - low)  # level1 0.382
        - support2 = p - level2 * (high - low)  # level2 0.618
        - support3 = p - level3 * (high - low)  # level3 1.000
        - resistance1 = p + level1 * (high - low)  # level1 0.382
        - resistance2 = p + level2 * (high - low)  # level2 0.618
        - resistance3 = p + level3 * (high - low)  # level3 1.000

    Additional information found at:
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:pivot_points
    https://www.investopedia.com/terms/p/pivotpoint.asp
    
    """

    lines = ('p', 's1', 's2', 's3', 'r1', 'r2', 'r3')
    params = (('open', False),  # add opening price to the pivot point
              ('close', False),  # use close twice in the calcs
              ('_autoplot', True),  # attempt to plot on real target data
              ('level1', 0.382),
              ('level2', 0.618),
              ('level3', 1.0))

    plotinfo = dict(subplot=False)

    def _plotinit(self):
        # Try to plot to the actual timeframe master
        if self.params._autoplot:
            if hasattr(self.data, 'data'):
                self.plotinfo.plotmaster = self.data.data

    def __init__(self):
        o = self.data.open
        h = self.data.high  # current high
        l = self.data.low  # current high
        c = self.data.close  # current high

        if self.params.close:
            self.lines.p = p = (h + l + 2.0 * c) / 4.0
        elif self.params.open:
            self.lines.p = p = (h + l + c + o) / 4.0
        else:
            self.lines.p = p = (h + l + c) / 3.0

        self.lines.s1 = p - self.params.level1 * (h - l)
        self.lines.s2 = p - self.params.level2 * (h - l)
        self.lines.s3 = p - self.params.level3 * (h - l)

        self.lines.r1 = p + self.params.level1 * (h - l)
        self.lines.r2 = p + self.params.level2 * (h - l)
        self.lines.r3 = p + self.params.level3 * (h - l)

        super(FibonacciPivotPoint, self).__init__()

        if self.params._autoplot:
            self.plotinfo.plot = False  # disable own plotting
            self()  # Coupler to follow real object


class DemarkPivotPoint(Indicator):

    """Demark Pivot Point - defines a level of significance by taking into
    account the average of price bar components of the past period of a larger
    timeframe. For example, when operating with days, the values are taken from
    the past month's fixed prices.

    Fibonacci levels (configurable) are used to define the support/resistance
    levels.

    Data must be resampled to use this indicator. For example:

        - data = bt.feeds.datafeed(dataname=x, timeframe=bt.TimeFrame.Days)
        - cerebro.adddata(data)
        - cerebro.resampledata(data, timeframe=bt.TimeFrame.Months)

    In the __init__ method of the strategy:

        - pivot = bt.ind.DemarkPivotPoint(self.data1)  # the resampled data

    This indicator will automatically try and plot the non-resampled data. To
    disable this bevaiour, use the following during construction:

        - _autoplot=False

    Notes:

        - The example shows days and months, but any combination of timeframes
          can be used

    Formula:

        - if close < open x = high + (2 x low) + close
        - if close > open x = (2 x high) + low + close
        - if Close == open x = high + low + (2 x close)
        - p = x / 4
        - support1 = x / 2 - high
        - resistance1 = x / 2 - low

    Additional information found at:
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:pivot_points
    
    """

    lines = ('p', 's1', 'r1')
    params = (('open', False),  # add opening price to the pivot point
              ('close', False),  # use close twice in the calcs
              ('_autoplot', True),  # attempt to plot on real target data
              ('level1', 0.382),
              ('level2', 0.618),
              ('level3', 1.0))

    plotinfo = dict(subplot=False)

    def _plotinit(self):
        # Try to plot to the actual timeframe master
        if self.params._autoplot:
            if hasattr(self.data, 'data'):
                self.plotinfo.plotmaster = self.data.data

    def __init__(self):
        x1 = self.data.high + 2.0 * self.data.low + self.data.close
        x2 = 2.0 * self.data.high + self.data.low + self.data.close
        x3 = self.data.high + self.data.low + 2.0 * self.data.close

        x = CmpEx(self.data.close, self.data.open, x1, x2, x3)
        self.lines.p = x / 4.0

        self.lines.s1 = x / 2.0 - self.data.high
        self.lines.r1 = x / 2.0 - self.data.low

        super(DemarkPivotPoint, self).__init__()

        if self.params._autoplot:
            self.plotinfo.plot = False  # disable own plotting
            self()  # Coupler to follow real object