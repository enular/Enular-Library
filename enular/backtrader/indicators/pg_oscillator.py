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

from . import Indicator, MovAv, ATR



class PrettyGoodOscillator(Indicator):

    """Pretty Good Oscillator - takes the distance of the current close from its
    simple moving average, measuring this value against the average true range,
    outputting the ratio.

    The suggested approach is to use this indicator as a breakout system for
    longer-term trades. If the PGO value rises above 3.0, a long position should
    be taken. If the value drops below -3.0, then a short position should be
    taken. In both cases, the exit condition is reached when the output returns
    to zero.

    The default period is set to 14, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - PrettyGoodOscillator(self.data, period=self.params.period)
        - PrettyGoodOscillator(self.data, period=self.p.period)
        - PrettyGoodOscillator(self.data, period=14)
        - PrettyGoodOscillator(self.data)

    Formula:
    
        - pgo = (data.close - sma(data, period)) / atr(data, period)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - PrettyGoodOscillator(self.data, _movav=WMA)

    Additional information found at:
    https://user42.tuxfamily.org/chart/manual/Pretty-Good-Oscillator.html
    https://earnfo.com/pretty-good-oscillator-pgo/
    
    """

    alias = ('PGO', 'PrettyGoodOsc', )
    lines = ('pgo', )
    params = (('period', 14), ('_movav', MovAv.Simple))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(pgo=dict(_name='=', color='navy'))

    def __init__(self):
        movav = self.params._movav(self.data, period=self.params.period)
        atr = ATR(self.data, period=self.params.period)

        self.lines.pgo = (self.data - movav) / atr
        
        super(PrettyGoodOscillator, self).__init__()