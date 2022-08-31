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


class PercentChange(Indicator):

    """Percent Change - measures the percentage change of the current value with
    that of n-period bars ago.

    The default period is set to 30, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - PercentChange(self.data, period=self.params.period)
        - PercentChange(self.data, period=self.p.period)
        - PercentChange(self.data, period=30)
        - PercentChange(self.data)

    Formula:
    
        - (data / data(-period)) - 1
    
    """

    alias = ('PctChange', )
    lines = ('pctchange', )
    params = (('period', 30), )

    plotlines = dict(pctchange=dict(_name='%Change', color='navy'))

    def __init__(self):
        self.lines.pctchange = self.data / self.data(-self.params.period) - 1.0
        
        super(PercentChange, self).__init__()