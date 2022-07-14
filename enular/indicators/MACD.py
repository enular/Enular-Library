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
from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
from Moving_Averages import EMA


class MACD(bt.Indicator):

    """
    Moving Average Convergence/Divergence - designed to reveal changes
    in the strength, direction, momentum, and duration of a trend. It 
    uses a short and a slightly longer-term Exponential Moving Average
    to identify a trend, and the buy/sell signal is realised when the
    longer, lagging moving average crosses the faster, leading moving
    average. Hence, the convergence and the subsequent divergence of
    the lines.

    This indicator requires 3 positional arguments that can be
    overridden when calling the function. The default values are:

        - m1_period = 12
        - m2_period = 26
        - signal_period = 9

    Calling the function requires 1 mandatory parameter, 'data,'
    with the additional optional parameters above. Examples:

    MACD(self.data, m1_period=self.params.m1_period)
    MACD(self.data, m1_period=self.p.m1_period, m2_period=self.p.m2_period, signal_period=self.p.signal_period)
    MACD(self.data, m1_period=12, m2_period=26, signal_period=9)
    MACD(self.data)

    Formula: macd = EMA(self.data, m1_period) - EMA(self.data, m2_period)
             signal = EMA(macd, signal_period)

    Additional information found at:
    https://en.wikipedia.org/wiki/MACD
    https://www.investopedia.com/terms/m/macd.asp
    
    """

    lines = ('macd', 'signal', )
    params = (('m1_period', 12),
              ('m2_period', 26),
              ('signal_period', 9), )

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(macd=dict(color='crimson'), signal=dict(ls='--', color='navy'))

    def __init__(self):
        m1 = EMA(self.data, period=self.params.m1_period)
        m2 = EMA(self.data, period=self.params.m2_period)

        self.lines.macd = m1 - m2
        self.lines.signal = EMA(self.lines.macd, period=self.params.signal_period)

class MACDHisto(MACD):

    """
    Provides the same output as the MACD base-class with the inclusion
    of a bar chart. This overlay represents the difference between the
    MACD and signal lines, and is refered to as the MACD-Histogram.

    Like the standard MACD, this indicator requires 3 positional
    arguments that can be overridden when calling the function.
    The default values are:

        - m1_period = 12
        - m2_period = 26
        - signal_period = 9

    Calling the function requires 1 mandatory parameter, 'data,'
    with the additional optional parameters above. Examples:

    MACDHisto(self.data, m1_period=self.params.m1_period)
    MACDHisto(self.data, m1_period=self.p.m1_period, m2_period=self.p.m2_period, signal_period=self.p.signal_period)
    MACDHisto(self.data, m1_period=12, m2_period=26, signal_period=9)
    MACDHisto(self.data)

    Formula = macd - signal

    Additional information found at:
    https://en.wikipedia.org/wiki/MACD#Terminology
    https://school.stockcharts.com/doku.php?id=technical_indicators:macd-histogram
    
    """

    lines = ('histogram', )
    plotlines = dict(histogram=dict(_method='bar', color='forestgreen', alpha=0.5, width=1.0))

    def __init__(self):
        # superclass to inherit the functions and parameters of the MACD base-class
        super(MACDHisto, self).__init__()
        
        self.lines.histogram = self.lines.macd - self.lines.signal