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
from . import SumN, Max



class Vortex(Indicator):

    """Vortex Indicator - consists of an uptrend line +VI and a downtrend line
    -VI, and is used to identify trend reversals and confirm current trends.

    The default period is set to 14, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period.'. Examples:

        - Vortex(self.data, period=self.params.period)
        - Vortex(self.data, period=self.p.period)
        - Vortex(self.data, period=14)
        - Vortex(self.data)

    Formula:

        - h0l1 = abs(data.high(0) - data.low(-1))
        - l0h1 = abs(data.low(0) - data.high(-1))
        - vm_plus = SumN(h0l1, period)
        - vm_minus = SumN(l0h1, period)
        - h0c1 = abs(data.high(0) - data.close(-1))
        - l0c1 = abs(data.low(0) - data.close(-1))
        - h0c0 = abs(data.high(0) - data.low(0))
        - tr = SumN(Max(h0l0, h0c1, l0c1), period)
        - +VI = vm_plus / tr
        - -VI = vm_minus / tr

    Additional information found at:
    https://www.investopedia.com/terms/v/vortex-indicator-vi.asp
    https://en.wikipedia.org/wiki/Vortex_indicator
    https://school.stockcharts.com/doku.php?id=technical_indicators:vortex_indicator
    
    """

    lines = ('vi_plus', 'vi_minus')
    params = (('period', 14), )

    plotlines = dict(vi_plus=dict(_name='+VI', color='crimson'),
                     vi_minus=dict(_name='-VI', color='navy'))

    def __init__(self):
        h0l1 = abs(self.data.high(0) - self.data.low(-1))
        vm_plus = SumN(h0l1, period=self.params.period)

        l0h1 = abs(self.data.low(0) - self.data.high(-1))
        vm_minus = SumN(l0h1, period=self.params.period)

        h0c1 = abs(self.data.high(0) - self.data.close(-1))
        l0c1 = abs(self.data.low(0) - self.data.close(-1))
        h0l0 = abs(self.data.high(0) - self.data.low(0))

        tr = SumN(Max(h0l0, h0c1, l0c1), period=self.params.period)

        self.lines.vi_plus = vm_plus / tr
        self.lines.vi_minus = vm_minus / tr

        super(Vortex, self).__init__()