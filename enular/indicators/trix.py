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



class TRIXSignal(Indicator):

    """A momentum oscillator showing the percent rate of change of a 3rd order
    Exponential Moving Average.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 15
        - roc_period = 1
        - signal_period = 10

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - TRIXSignal(self.data, period=self.params.period)
        - TRIXSignal(self.data, period=self.p.period, roc_period=self.p.roc_period, signal_period=self.p.signal_period)
        - TRIXSignal(self.data, period=15, roc_period=1, signal_period=10)
        - TRIXSignal(self.data)
    
    Formula:
    
        - trix = 100 * EMA(EMA(EMA)) / EMA(EMA(EMA))[-period] - 1
        - signal = EMA(trix, signal_period)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - TRIXSignal(self.data, _movav=WMA)
    
    Additional information found at:
    https://school.stockcharts.com/doku.php?id=technical_indicators:trix
    https://en.wikipedia.org/wiki/Trix_(technical_analysis)
    
    """
 
    lines = ('trix', 'signal')
    params = (('period', 15),
              ('roc_period', 1),
              ('signal_period', 10),
              ('_movav', MovAv.Exponential))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(trix=dict(color='crimson'),
                     signal=dict(ls='--', color='navy'))

    def __init__(self):

        ema1 = self.params._movav(self.data, period=self.params.period)
        ema2 = self.params._movav(ema1, period=self.params.period)
        ema3 = self.params._movav(ema2, period=self.params.period)

        self.lines.trix = 100.0 * (ema3 / ema3(-self.params.roc_period) - 1.0)
        self.lines.signal = self.params._movav(self.lines.trix,
                                               period=self.params.signal_period)

        super(TRIXSignal, self).__init__()