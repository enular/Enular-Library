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
from . import MovAv, PercentRank



class DV2(Indicator):

    """DV2 - developed by David Varadi. Used to measure relative discrepancies
    between co-integrated, mean reverting assets. Therefore, it should be used
    in a long-term mean reverting strategy.

    It uses the percent rank function, measuring the current value against that
    of period bars ago.

    This indicator requires 2 positional arguments that can be overridden when
    calling the function. The default values are:

        - period = 252
        - ma_period = 2

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DV2(self.data, period=self.params.period)
        - DV2(self.data, period=self.p.period, ma_period=self.p.ma_period)
        - DV2(self.data, period=252, ma_period=2)
        - DV2(self.data)

    Formula:

        - chl = close / ((high + low) / 2)
        - dvu = SMA(chl, ma_period)
        - DV2 = PercentRank(dvu, period)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DV2(self.data, _movav=WMA)

    Additional information found at:
    https://cssanalytics.wordpress.com/2010/11/22/dv2-performance-in-review/
    
    """

    lines = ('dv2', )
    params = (('period', 252),
              ('ma_period', 2),
              ('_movav', MovAv.Simple))
    
    plotinfo = dict(plotymargin=0.1, plotyhlines=[0, 50, 100])
    plotlines = dict(dv2=dict(_name='=', color='navy'))

    def __init__(self):
        chl = self.data.close / ((self.data.high + self.data.low) / 2.0)
        dvu = self.params._movav(chl, period=self.params.ma_period)
        self.lines.dv2 = PercentRank(dvu, period=self.params.period) * 100

        super(DV2, self).__init__()