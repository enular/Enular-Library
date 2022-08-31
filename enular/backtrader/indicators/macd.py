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
from . import MovAv



class MACD(Indicator):

    """ Moving Average Convergence/Divergence - designed to reveal changes in
    the strength, direction, momentum, and duration of a trend. It uses a
    short and a slightly longer-term Exponential Moving Average to identify
    a trend, and the buy/sell signal is realised when the longer, lagging
    moving average crosses the faster, leading moving average. Hence, the
    convergence and the subsequent divergence of the lines.

    This indicator requires 3 positional arguments that can be overridden when
    calling the function. The default values are:

        - m1_period = 12
        - m2_period = 26
        - signal_period = 9

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - MACD(self.data, m1_period=self.params.m1_period)
        - MACD(self.data, m1_period=self.p.m1_period, m2_period=self.p.m2_period)
        - MACD(self.data, m1_period=12, m2_period=26, signal_period=9)
        - MACD(self.data)

    Formula:
    
        - macd = EMA(self.data, m1_period) - EMA(self.data, m2_period)
        - signal = EMA(macd, signal_period)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - MACD(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/MACD
    https://www.investopedia.com/terms/m/macd.asp
    
    """

    lines = ('macd', 'signal')
    params = (('m1_period', 12),
              ('m2_period', 26),
              ('signal_period', 9),
              ('_movav', MovAv.Exponential))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(macd=dict(color='crimson'),
                     signal=dict(ls='--', color='navy'))

    def __init__(self):
        m1 = self.params._movav(self.data, period=self.params.m1_period)
        m2 = self.params._movav(self.data, period=self.params.m2_period)

        self.lines.macd = m1 - m2
        self.lines.signal = self.params._movav(self.lines.macd,
                                               period=self.params.signal_period)

        super(MACD, self).__init__()
        


class MACDHisto(MACD):

    """Provides the same output as the MACD base-class with the inclusion of a
    bar chart. This overlay represents the difference between the MACD and
    signal lines, and is refered to as the MACD-Histogram.

    Like the standard MACD, this indicator requires 3 positional arguments that
    can be overridden when calling the function. The default values are:

        - m1_period = 12
        - m2_period = 26
        - signal_period = 9

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - MACDHisto(self.data, m1_period=self.params.m1_period)
        - MACDHisto(self.data, m1_period=self.p.m1_period, m2_period=self.p.m2_period)
        - MACDHisto(self.data, m1_period=12, m2_period=26, signal_period=9)
        - MACDHisto(self.data)

    Formula:
    
        - histogram = macd - signal

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - MACDHisto(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/MACD#Terminology
    https://school.stockcharts.com/doku.php?id=technical_indicators:macd-histogram
    
    """

    alias = ('MACDHistogram', )
    lines = ('histogram', )
    plotlines = dict(histogram=dict(_method='bar',
                                    color='forestgreen',
                                    alpha=0.5,
                                    width=1.0))

    def __init__(self):
        super(MACDHisto, self).__init__()
        
        self.lines.histogram = self.lines.macd - self.lines.signal