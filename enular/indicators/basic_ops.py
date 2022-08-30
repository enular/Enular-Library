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

import functools
import math
import operator

from ..utils.py3 import map, range

from . import Indicator



class PeriodN(Indicator):

    """Base class for indicators which take a period (__init__ has to be called
    explicitly or by superclass)
    
    This class has no defined lines.
    
    """

    params = (('period', 1), )

    def __init__(self):
        super(PeriodN, self).__init__()

        self.addminperiod(self.params.period)


class OperationN(PeriodN):

    """Calculates the 'func' for a given period. This serves as a base for
    classes that work with a period and can express the logic in a callable
    object.

    Note:

        - Base classes must provide a 'func' attribute which is a callable

    Formula:

        - line = func(data, period)
    
    """

    def next(self):
        self.line[0] = self.func(self.data.get(size=self.params.period))

    def once(self, start, end):
        dst = self.line.array
        src = self.data.array
        period = self.params.period
        func = self.func

        for i in range(start, end):
            dst[i] = func(src[i - period + 1: i + 1])


class BaseApplyN(OperationN):

    """Base class for ApplyN and others which may take a 'func' as a parameter
    but want to define the lines in the indicator.
    
    Calculates 'func' for a given period where func is given as a parameter,
    i.e. a named argument or 'kwarg'.

    Formula:

        - lines[0] = func(data, period)

    Any extra lines defined beyond the first (index 0) are not calculated.
    
    """

    params = (('func', None), )

    def __init__(self):
        self.func = self.params.func

        super(BaseApplyN, self).__init__()


class ApplyN(BaseApplyN):

    """Calculates 'func' for a given period.

    Formula:

        - line = func(data, period)
    
    """

    lines = ('apply', )


class Highest(OperationN):

    """Calculates the highest value for the data in a given period.

    Uses the built-in 'max' for the calculation.

    Formula:

        - highest = max(data, period)
    
    """

    alias = ('MaxN', )
    lines = ('highest', )

    func = max


class Lowest(OperationN):

    """Calculates the lowest value for the data in a given period.

    Uses the built-in 'low' for the calculation.

    Formula:

        - lowest = low(data, period)

    """

    alias = ('MinN', )
    lines = ('lowest', )
    
    func = min


class ReduceN(OperationN):

    """Calculates the reduced value of the 'period' data points by applying
    'function'. Uses the built-in 'reduce' for the calculation plus the 'func'
    that subclasses define.

    Formula:

        - reduced = reduce(function(data, period), initializer=initializer)

    Notes:

        - In order to mimic the python 'reduce', this indicator takes a
          'function' non-named argument as the first argument, unlike other
          indicators which take only named arguments.
    
    """

    lines = ('reduced', )

    func = functools.reduce

    def __init__(self, function, **kwargs):
        if 'initializer' not in kwargs:
            self.func = functools.partial(self.func, function)
        else:
            self.func = functools.partial(self.func, function,
                                          initializer=kwargs['initializer'])

        super(ReduceN, self).__init__()


class SumN(OperationN):

    """Calculates the sum of the data values over a given period. Uses
    'math.sum' for the calculation rather than the built-in 'sum' to avoid
    precision errors.

    Formula:

        - SumN = sum(data, period)
    
    """

    lines = ('sumn', )

    func = math.fsum


class AnyN(OperationN):

    """Has a value of 'True' (stored as 1.0 in the lines) if *any* of the values
    in the 'period' evaluates to non-zero (i.e. 'True'). Uses the built-in 'any'
    for the calculation.

    Formula:

        - AnyN = any(data, period)
    
    """

    lines = ('anyn', )

    func = any


class AllN(OperationN):

    """Has a value of 'True' (stored as 1.0 in the lines) if *all* of the values
    in the 'period' evaluates to non-zero (i.e. 'True'). Uses the built-in 'all'
    for the calculation.

    Formula:

        - AllN = all(data, period)
    
    """

    lines = ('alln', )

    func = all


class FindFirstIndex(OperationN):

    """Returns the index of the last data that satisfies equality with the
    condition generated by the parameter _evalfunc.

    Notes:

        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = first for which data[index] == _evalfunc(data)
    
    """

    lines = ('index', )
    params = (('_evalfunc', None), )

    def func(self, iterable):
        m = self.params._evalfunc(iterable)
        return next(i for i, v in enumerate(reversed(iterable)) if v == m)


class FindFirstIndexHighest(FindFirstIndex):

    """Returns the index of the first data that is the highest in the period.

    Notes:

        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = index of the first data which is the highest
    
    """

    params = (('_evalfunc', max), )


class FindFirstIndexLowest(FindFirstIndex):

    """Returns the index of the first data that is the lowest in the period.

    Notes:
        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = index of the first data which is the lowest
        
    """

    params = (('_evalfunc', min), )


class FindLastIndex(OperationN):

    """Returns the index of the last data that satisfies equality with the
    condition generated by the parameter _evalfunc.

    Notes:

        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = last for which data[index] == _evalfunc(data)
        
    """

    lines = ('index', )
    params = (('_evalfunc', None), )

    def func(self, iterable):
        m = self.params._evalfunc(iterable)
        index = next(i for i, v in enumerate(iterable) if v == m)
        # The iterable goes from 0 -> period - 1. If the last element
        # which is the current bar is returned and without the -1 then
        # period - index = 1 ... and must be zero!
        return self.params.period - index - 1


class FindLastIndexHighest(FindLastIndex):

    """Returns the index of the last data that is the highest in the period.

    Notes:

        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = index of last data which is the highest
        
    """

    params = (('_evalfunc', max), )


class FindLastIndexLowest(FindLastIndex):

    """Returns the index of the last data that is the lowest in the period.

    Notes:

        - Returned indexes look backwards. 0 is the current index and 1 is the
          previous bar.

    Formula:

        - index = index of last data which is the lowest
        
    """

    params = (('_evalfunc', min), )


class Accum(Indicator):

    """Cummulative sum of the data values.

    Formula:

        - accum += data

    """

    alias = ('CumSum', 'CumulativeSum')
    lines = ('accum', )
    params = (('seed', 0.0), )

    # xxxstart methods use the seed (starting value) and passed data to
    # construct the first value keeping the minperiod to 1 since no
    # initial look-back value is needed

    def nextstart(self):
        self.line[0] = self.params.seed + self.data[0]

    def next(self):
        self.line[0] = self.line[-1] + self.data[0]

    def oncestart(self, start, end):
        dst = self.line.array
        src = self.data.array
        prev = self.params.seed

        for i in range(start, end):
            dst[i] = prev = prev + src[i]

    def once(self, start, end):
        dst = self.line.array
        src = self.data.array
        prev = dst[start - 1]

        for i in range(start, end):
            dst[i] = prev = prev + src[i]


class Average(PeriodN):

    """Averages a given data set arithmetically over a period.

    Formula:

        - average = data(period) / period

    Additional information found at:
    https://en.wikipedia.org/wiki/Arithmetic_mean
    
    """

    alias = ('ArithmeticMean', 'Mean')
    lines = ('av', )

    def next(self):
        self.line[0] = \
            math.fsum(self.data.get(size=self.params.period)) / self.params.period

    def once(self, start, end):
        src = self.data.array
        dst = self.line.array
        period = self.params.period

        for i in range(start, end):
            dst[i] = math.fsum(src[i - period + 1:i + 1]) / period


class ExponentialSmoothing(Average):

    """Averages a given data set over a period using exponential smoothing.
    A regular arithmetic mean is used as the seed value considering the first
    period values of the data.

    Formula:

        - average = prev * (1 - alpha) + data * alpha

    Additional information found at:
    https://en.wikipedia.org/wiki/Exponential_smoothing
    
    """

    alias = ('ExpSmoothing', )
    params = (('alpha', None), )

    def __init__(self):
        self.alpha = self.params.alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + self.params.period)  # def EMA value

        self.alpha1 = 1.0 - self.alpha

        super(ExponentialSmoothing, self).__init__()

    def nextstart(self):
        # Fetch the seed value from the base class calculation
        super(ExponentialSmoothing, self).next()

    def next(self):
        self.line[0] = self.line[-1] * self.alpha1 + self.data[0] * self.alpha

    def oncestart(self, start, end):
        # Fetch the seed value from the base class calculation
        super(ExponentialSmoothing, self).once(start, end)

    def once(self, start, end):
        darray = self.data.array
        larray = self.line.array
        alpha = self.alpha
        alpha1 = self.alpha1

        # Seed value from SMA calculated with the call to oncestart
        prev = larray[start - 1]
        for i in range(start, end):
            larray[i] = prev = prev * alpha1 + darray[i] * alpha


class ExponentialSmoothingDynamic(ExponentialSmoothing):

    """Averages a given data set over a period using exponential smoothing.
    A regular arithmetic mean is used as the seed value considering the first
    period values of the data.

    Notes:

        - Alpha is an array of values which can be calculated dynamically

    Formula:

        - average = prev * (1 - alpha) + data * alpha

    Additional information found at:
    https://en.wikipedia.org/wiki/Exponential_smoothing
    
    """

    alias = ('ExpSmoothingDynamic', )

    def __init__(self):
        super(ExponentialSmoothingDynamic, self).__init__()

        # Hack: alpha is a "line" and carries a minperiod which is not being
        # considered because this indicator makes no line assignment. It has
        # therefore to be considered manually
        minperioddiff = max(0, self.alpha._minperiod - self.params.period)
        self.lines[0].incminperiod(minperioddiff)

    def next(self):
        self.line[0] = \
            self.line[-1] * self.alpha1[0] + self.data[0] * self.alpha[0]

    def once(self, start, end):
        darray = self.data.array
        larray = self.line.array
        alpha = self.alpha.array
        alpha1 = self.alpha1.array

        # Seed value from SMA calculated with the call to oncestart
        prev = larray[start - 1]
        for i in range(start, end):
            larray[i] = prev = prev * alpha1[i] + darray[i] * alpha[i]


class WeightedAverage(PeriodN):

    """Calculates the weighted average of the given data set over a period.
    The default weights (if none are provided) are linear to assign more
    weight to the most recent data point. The result will be multiplied
    by a given coefficient.

    Formula:

        - average = coef * sum(mul(data, period), weights)

    Additional information found at:
    https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
    
    """

    alias = ('AverageWeighted', )
    lines = ('av', )
    params = (('coef', 1.0), ('weights', tuple()))

    def __init__(self):
        super(WeightedAverage, self).__init__()

    def next(self):
        data = self.data.get(size=self.params.period)
        dataweighted = map(operator.mul, data, self.params.weights)
        self.line[0] = self.params.coef * math.fsum(dataweighted)

    def once(self, start, end):
        darray = self.data.array
        larray = self.line.array
        period = self.params.period
        coef = self.params.coef
        weights = self.params.weights

        for i in range(start, end):
            data = darray[i - period + 1: i + 1]
            larray[i] = coef * math.fsum(map(operator.mul, data, weights))