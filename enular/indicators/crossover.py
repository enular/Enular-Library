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
                        
from . import Indicator, And


class NonZeroDifference(Indicator):

    """Keeps track of the difference between two data inputs, using the last
    non-zero value if the current difference is zero.

    Formula:

        - diff = data0 - data1
        - NZD = diff if diff != zero else diff(-1)
    
    """
 
    _mindatas = 2  # requires two (2) data sources

    alias = ('NZD', )
    lines = ('nzd', )

    def nextstart(self):
        self.lines.nzd[0] = self.data0[0] - self.data1[0]  # seed value

    def next(self):
        d = self.data0[0] - self.data1[0]
        self.lines.nzd[0] = d if d else self.lines.nzd[-1]

    def oncestart(self, start, end):
        self.line.array[start] = (self.data0.array[start] - self.data1.array[start])

    def once(self, start, end):
        d0array = self.data0.array
        d1array = self.data1.array
        larray = self.line.array

        prev = larray[start - 1]
        for i in range(start, end):
            d = d0array[i] - d1array[i]
            larray[i] = prev = d if d else prev


class _CrossBase(Indicator):

    """Base class for CrossUp, CrossDown and CrossOver classes."""
    
    _mindatas = 2

    lines = ('cross', )

    plotinfo = dict(plotymargin=0.05, plotyhlines=[0.0, 1.0])
    plotlines = dict(cross=dict(color='navy'))

    def __init__(self):
        nzd = NonZeroDifference(self.data0, self.data1)

        if self._crossup:
            before = nzd(-1) < 0.0  # data0 was below or at 0
            after = self.data0 > self.data1
        else:
            before = nzd(-1) > 0.0  # data0 was above or at 0
            after = self.data0 < self.data1

        self.lines.cross = And(before, after)


class CrossUp(_CrossBase):

    """Cross Up - provides a signal if the first input data cross over the
    second input data upwards.

    Looks at the current period index (0) and the previous period index (-1) of
    both data sources.

    Calling the function requires 2 mandatory parameters. Examples:

        - CrossUp(SMA(self.data, period=50), SMA(self.data, period=100))
        - CrossUp(self.data0, self.data1)

    Formula:

        - diff = data0 - data1
        - up cross = last non-zero diff < 0 and data0(0) > data1(0)

    """

    _crossup = True


class CrossDown(_CrossBase):

    """Cross Down - provides a signal if the first input data cross over the
    second input data downwards.

    Looks at the current period index (0) and the previous period index (-1) of
    both data sources.

    Requires two mandatory parameters. Examples:

        - CrossDown(SMA(self.data, period=50), SMA(self.data, period=100))
        - CrossDown(self.data0, self.data1)

    Formula:

        - diff = data0 - data1
        - down cross = last non-zero diff > 0 and data0(0) < data1(0)

    """

    _crossup = False


class CrossOver(Indicator):

    """Crossover - creates a signal if the provided datas cross up or down. For
    example:

        - 1.0 if the first data source crosses over the second data source
          upwards
        - -1.0 if the first data source crosses over the second data source
          downwards 
    
    Looks at the current period index (0) and the previous period index (-1) of
    both data sources.

    Requires two mandatory parameters. Examples:

        - CrossOver(SMA(self.data, period=50), SMA(self.data, period=100))
        - CrossOver(self.data0, self.data1)

    Formula:

        - diff = data0 - data1
        - up cross = last non-zero diff < 0 and data0(0) > data1(0)
        - down cross = last non-zero diff > 0 and data0(0) < data1(0)
        - crossover = up cross - down cross
    
    """

    _mindatas = 2

    lines = ('crossover', )

    plotinfo = dict(plotymargin=0.05, plotyhlines=[-1.0, 1.0])
    plotlines = dict(crossover=dict(color='navy'))

    def __init__(self):
        upcross = CrossUp(self.data, self.data1)
        downcross = CrossDown(self.data, self.data1)

        self.lines.crossover = upcross - downcross