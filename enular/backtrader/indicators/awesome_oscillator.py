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



class AwesomeOscillator(Indicator):

    """Awesome Oscillator - used to measure market momentum by calculating the
    difference between a fast and slow SMA, using the midpoint of each bar.

    This indicator requires two positional arguments that can be overridden
    when calling the function. The default values are:

        - fast = 5
        - slow = 34

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AwesomeOscillator(self.data, fast=self.params.fast, slow=self.params.slow)
        - AwesomeOscillator(self.data, fast=self.p.fast, slow=self.p.slow)
        - AwesomeOscillator(self.data, fast=5, slow=34)
        - AwesomeOscillator(self.data)

    Formula:
    
        - median price = (high + low) / 2
        - AO = SMA(median price, fast period) - SMA(median price, slow period)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use EMA by including _movav=EMA in the
          function.
        - AwesomeOscillator(self.data, _movav=EMA)

    Additional information found at:
    https://www.tradingview.com/support/solutions/43000501826-awesome-oscillator-ao/
    https://www.ig.com/uk/trading-strategies/a-traders-guide-to-using-the-awesome-oscillator-200130
    
    """

    alias = ('AwesomeOsc', 'AO')
    lines = ('ao', )
    params = (('fast', 5), ('slow', 34), ('_movav', MovAv.SMA))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(ao=dict(_name='=',
                             _method='bar',
                             color='white',
                             _fill_gt=(0, ('forestgreen', 0.7)),
                             _fill_lt=(0, ('crimson', 0.7)),
                             alpha=0.5,
                             width=1.0))

    def __init__(self):
        median_price = (self.data.high + self.data.low) / 2.0
        sma1 = self.params._movav(median_price, period=self.params.fast)
        sma2 = self.params._movav(median_price, period=self.params.slow)

        self.lines.ao = sma1 - sma2

        super(AwesomeOscillator, self).__init__()