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
from . import MovAv, StdDev



class BollingerBands(Indicator):

    """Bollinger Bands - a pricing envelope showing the upper and lower price
    ranges from a moving average. Each price band is fixed at x amount of
    standard deviations and adjusts according to swings in volatility of the
    underlying price. Bollinger Bands help to identify whether prices are high
    or low on a relative basis.

    This indicator requires two positional arguments that can be overridden when
    calling the function. The default values are:

        - period = 20
        - stddev = 2.0

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - BollingerBands(self.data, period=self.params.period)
        - BollingerBands(self.data, period=self.p.period, stddev=self.p.stddev)
        - BollingerBands(self.data, period=20, stddev=2.0)
        - BollingerBands(self.data)

    Formula:
    
        - middle = SMA(data, period)
        - top = middle + stddev
        - bottom = middle - stddev

    Where:

        - stddev = self.p.stddev * StandardDeviation(data, middle, period, SMA)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - BollingerBands(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Bollinger_Bands
    https://www.investopedia.com/terms/b/bollingerbands.asp
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-bands#
    
    """

    alias = ('BBands', )
    lines = ('middle', 'top', 'bottom')
    params = (('period', 20), ('stddev', 2.0), ('_movav', MovAv.Simple))

    plotinfo = dict(subplot=False)
    plotlines = dict(middle=dict(ls='--', color='crimson'),
                     top=dict(color='blue'),
                     bottom=dict(color='blue'))

    def __init__(self):
        self.lines.middle = ma = self.params._movav(self.data, period=self.params.period)
        stddev = self.params.stddev * StdDev(self.data, ma, period=self.params.period, _movav=self.params._movav)
        self.lines.top = ma + stddev
        self.lines.bottom = ma - stddev

        super(BollingerBands, self).__init__()


class BBPerc(Indicator):

    """Bollinger Bands %B - quantifies the price change relative to the upper
    and lower band. There are six basic characteristics:

        - %B equals 1 when price is at the upper band
        - %B equals 0 when price is at the lower band
        - %B is above 1 when price is above the upper band
        - %B is below 0 when price is below the lower band
        - %B is above .50 when price is above the middle band
        - %B is below .50 when price is below the middle band

    This indicator requires two positional arguments that can be overridden when
    calling the function. The default values are:

        - period = 20
        - stddev = 2.0

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - BBPerc(self.data, period=self.params.period)
        - BBPerc(self.data, period=self.p.period, stddev=self.p.stddev)
        - BBPerc(self.data, period=20, stddev=2.0)
        - BBPerc(self.data)

    Formula:
    
        - %B = (price - bottom) / (top - bottom)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - BBPerc(self.data, _movav=WMA)

    Additional information found at:
    https://www.barchart.com/education/technical-indicators/bollinger_bands_percent
    
    """

    alias = ('BBperc', )
    lines = ('perc_bb', )
    params = (('period', 20), ('stddev', 2.0), ('_movav', MovAv.Simple))

    plotinfo = dict(plotymargin=0.05, plotyhlines=[0, 0.5, 1])
    plotlines = dict(perc_bb=dict(_name='%B', color='navy'))

    def __init__(self):
        ma = self.params._movav(self.data, period=self.params.period)
        stddev = self.params.stddev * StdDev(self.data,
                                             ma,
                                             period=self.params.period,
                                             _movav=self.params._movav)
        top = ma + stddev
        bottom = ma - stddev
        self.lines.perc_bb = (self.data - bottom) / (top - bottom)

        super(BBPerc, self).__init__()


class BBWidth(Indicator):
 
    """Bollinger Bands Width - the difference between the top and the bottom
    bands divided by the middle band. This variation aims to visualise
    consolidation before price movements, represented by low bandwidth values,
    or periods of high volatility, represented by high bandwidth values.
    
    This indicator requires two positional arguments that can be overridden when
    calling the function. The default values are:

        - period = 20
        - stddev = 2.0

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - BBWidth(self.data, period=self.params.period)
        - BBWidth(self.data, period=self.p.period, stddev=self.p.stddev)
        - BBWidth(self.data, period=20, stddev=2.0)
        - BBWidth(self.data)

    Formula:
    
        - BBW = (top - bottom) / middle

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - BBWidth(self.data, _movav=WMA)

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-band-width
    
    """

    alias = ('BBwidth', )
    lines = ('bbw', )
    params = (('period', 20), ('stddev', 2.0), ('_movav', MovAv.Simple))
    
    plotlines = dict(bbw=dict(_name='BBW',
                              _method='bar',
                              color='forestgreen',
                              alpha=0.7,
                              width=1.0))

    def __init__(self):
        middle = ma = self.params._movav(self.data, period=self.params.period)
        stddev = self.params.stddev * StdDev(self.data,
                                             ma,
                                             period=self.params.period,
                                             _movav=self.params._movav)
        top = ma + stddev
        bottom = ma - stddev
        self.lines.bbw = (top - bottom) / middle

        super(BBWidth, self).__init__()