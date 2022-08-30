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

from . import PeriodN



class LaguerreRSI(PeriodN):

    """Laguerre RSI - a variation of the Relative Strength Index, this indicator
    attempts to avoid whipsaws and lags associated with the standard RSI.

    This indicator requires 2 positional arguments that can be overridden when
    calling the function. The default values are:

        - gamma = 0.5
        - period = 6

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - LaguerreRSI(self.data, gamma=self.params.gamma)
        - LaguerreRSI(self.data, gamma=self.p.gamma, period=self.p.period)
        - LaguerreRSI(self.data, gamma=0.5, period=6)
        - LaguerreRSI(self.data)


    Additional information found at:
    https://www.litefinance.com/blog/for-beginners/best-technical-indicators/laguerre-indicator/

    """

    alias = ('LRSI', )
    lines = ('lrsi', )
    params = (('gamma', 0.5), ('period', 6))

    plotinfo = dict(plotymargin=0.15, plotyticks=[0.0, 0.2, 0.5, 0.8, 1.0])
    plotlines = dict(lrsi=dict(_name='=', color='navy'))

    l0, l1, l2, l3 = 0.0, 0.0, 0.0, 0.0

    def next(self):
        l0_1 = self.l0  # cache previous intermediate values
        l1_1 = self.l1
        l2_1 = self.l2

        g = self.params.gamma  # avoid more lookups
        self.l0 = l0 = (1.0 - g) * self.data + g * l0_1
        self.l1 = l1 = -g * l0 + l0_1 + g * l1_1
        self.l2 = l2 = -g * l1 + l1_1 + g * l2_1
        self.l3 = l3 = -g * l2 + l2_1 + g * self.l3

        cu = 0.0
        cd = 0.0

        if l0 >= l1:
            cu = l0 - l1
        else:
            cd = l1 - l0

        if l1 >= l2:
            cu += l1 - l2
        else:
            cd += l2 - l1

        if l2 >= l3:
            cu += l2 - l3
        else:
            cd += l3 - l2

        den = cu + cd

        self.lines.lrsi[0] = 1.0 if not den else cu / den



class LaguerreFilter(PeriodN):

    """Laguerre Filter - functions like a moving average, attempting to filter
    out noise from pricing data using a smoothing component, gamma.

    The default value for gamma is set to 0.5, but can be overridden when
    calling the function. Values between 0.2 and 0.8 have been suggested by the
    author, John F. Ehlers.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - LaguerreFilter(self.data, gamma=self.params.gamma)
        - LaguerreFilter(self.data, gamma=self.p.gamma)
        - LaguerreFilter(self.data, period=0.5)
        - LaguerreFilter(self.data)


    Additional information found at:
    https://www.litefinance.com/blog/for-beginners/best-technical-indicators/laguerre-indicator/

    """

    alias = ('LAGF', )
    lines = ('filter', )
    params = (('gamma', 0.5), )

    plotinfo = dict(subplot=False)
    plotlines = dict(filter=dict(color='navy'))

    l0, l1, l2, l3 = 0.0, 0.0, 0.0, 0.0

    def _plotlabel(self):
        plabels = [self.params.gamma]
        return plabels

    def next(self):
        l0_1 = self.l0  # cache previous intermediate values
        l1_1 = self.l1
        l2_1 = self.l2

        g = self.params.gamma  # avoid more lookups
        self.l0 = l0 = (1.0 - g) * self.data + g * l0_1
        self.l1 = l1 = -g * l0 + l0_1 + g * l1_1
        self.l2 = l2 = -g * l1 + l1_1 + g * l2_1
        self.l3 = l3 = -g * l2 + l2_1 + g * self.l3
        self.lines.filter[0] = (l0 + (2 * l1) + (2 * l2) + l3) / 6