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
from . import MovAv, Max, Min

from backtrader.utils.py3 import range



class HeikinAshi(Indicator):

    """Heikin Ashi - in line form. Necessary for the Heikin Ashi Delta
    indicator.

    Formula:

        - ha_open = (ha_open[-1] + ha_close[-1]) / 2
        - ha_close = (open + high + low + close) / 4
        - ha_high = Max(data.high, ha_open, ha_close)
        - ha_low = Min(data.low, ha_open, ha_close)
    
    Additional information found at:
    https://www.investopedia.com/trading/heikin-ashi-better-candlestick/
    https://school.stockcharts.com/doku.php?id=chart_analysis:heikin_ashi
    
    """

    lines = ('ha_open',
             'ha_high',
             'ha_low',
             'ha_close')

    linealias = (('ha_open', 'open'),
                 ('ha_high', 'high'),
                 ('ha_low', 'low'),
                 ('ha_close', 'close'))

    plotinfo = dict(subplot=False)

    _nextforce = True

    def __init__(self):
        o = self.data.open
        h = self.data.high
        l = self.data.low
        c = self.data.close

        self.lines.ha_close = ha_close = (o + h + l + c) / 4.0
        self.lines.ha_open = ha_open = (self.lines.ha_open(-1) + ha_close(-1)) / 2.0
        self.lines.ha_high = Max(h, ha_open, ha_close)
        self.lines.ha_low = Min(l, ha_open, ha_close)

        super(HeikinAshi, self).__init__()

    def prenext(self):
        # seed recursive value
        self.lines.ha_open[0] = (self.data.open[0] + self.data.close[0]) / 2.0


class HADelta(Indicator):

    """Heikin Ashi Delta - measures the difference between the Heikin Ashi open
    and close, or the body of the candlestick. Two lines are generated, a fast
    HA Delta line, comprising of the difference between the open and the close,
    and a smoothed line using a Simple Moving Average over 3 periods.

    When the fast (HA Delta) line crosses the slow (smoothed), this signals the
    possibility of a changing trend.

    The default period is set to 3, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - HADelta(self.data, period=self.params.period)
        - HADelta(self.data, period=self.p.period)
        - HADelta(self.data, period=3)
        - HADelta(self.data)

    Formula:

        - HADelta = Heikin Ashi close - Heikin Ashi open
        - Smoothed = SMA(HADelta, period)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - HADelta(self.data, _movav=WMA)

    Additional information found at:
    https://www.prescientrading.com/kb/heikin-ashi-and-ha-delta/
    
    """

    alias = ('haD', )
    lines = ('haDelta', 'smoothed')
    params = (('period', 3),
              ('_movav', MovAv.Simple),
              ('autoheikin', True))

    plotinfo = dict(subplot=True)
    plotlines = dict(haDelta=dict(_name='HeikinAshiDelta',
                                  color='royalblue'),
                    smoothed=dict(_name='Smoothed',
                                  color='dimgray',
                                  _fill_gt=(0, ('forestgreen', 0.5)),
                                  _fill_lt=(0, ('crimson', 0.5))))
    
    def _plotlabel(self):
        plabels = [self.params.period, self.params._movav]
        return plabels

    def __init__(self):
        d = HeikinAshi(self.data) if self.params.autoheikin else self.data

        self.lines.haDelta = hd = d.close - d.open
        self.lines.smoothed = self.params._movav(hd, period=self.params.period)

        super(HADelta, self).__init__()