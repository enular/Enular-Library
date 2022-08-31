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



class StandardDeviation(Indicator):

    """Standard Deviation - calculates the standard deviation of data over a
    given period.

    If two sets of data are provided, the second is considered to be the mean
    of the first.

    Two arguments are required that can be overridden when calling the function.
    The default values are:

        - period = 20
        - safepow = True

    The default of 'safepow' is 'True'. If this parameter is set to 'False', the
    standard deviation will be calculated as:

        - pow((meansq - sqmean), 0.5)

    Setting the value to 'True' safeguards against the possibility of a negative
    value in the (meansq - sqmean) calculation.

    Formula:

        - mean squared = SMA(pow(data, 2), period)
        - squared mean = pow(SMA(data, period), 2)
        - StdDev = pow(mean squared - squared mean, 0.5)

    Additional information found at:
    https://en.wikipedia.org/wiki/Standard_deviation
    
    """

    alias = ('StdDev', )
    lines = ('stddev', )
    params = (('period', 20),
              ('_movav', MovAv.Simple),
              ('safepow', True))

    plotlines = dict(stddev=dict(color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        return plabels

    def __init__(self):
        if len(self.datas) > 1:
            mean = self.data1
        else:
            mean = self.params._movav(self.data, period=self.params.period)

        meansq = self.params._movav(pow(self.data, 2), period=self.params.period)
        sqmean = pow(mean, 2)

        if self.params.safepow:
            self.lines.stddev = pow(abs(meansq - sqmean), 0.5)
        else:
            self.lines.stddev = pow(meansq - sqmean, 0.5)

        super(StandardDeviation, self).__init__()



class MeanDeviation(Indicator):

    """Mean Deviation - calculates the mean deviation of data over a given
    period.

    If two sets of data are provided, the second is considered to be the mean
    of the first.

    The default period is set to 20, but can be overridden when calling the
    function.

    Formula:

        - mean = SMA(data, period) (or provided mean value)
        - abs deviation = abs(data - mean)
        - MeanDev = SMA(abs deviation, period)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_absolute_deviation
    
    """

    alias = ('MeanDev', )
    lines = ('meandev', )
    params = (('period', 20), ('_movav', MovAv.Simple))

    plotlines = dict(meandev=dict(color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        return plabels

    def __init__(self):
        if len(self.datas) > 1:
            mean = self.data1
        else:
            mean = self.params._movav(self.data, period=self.params.period)

        absdev = abs(self.data - mean)
        self.lines.meandev = self.params._movav(absdev, period=self.params.period)

        super(MeanDeviation, self).__init__()