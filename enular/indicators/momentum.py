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

from . import Indicator



class Momentum(Indicator):

    """Momentum Indicator - measures the strength of a trend in absolute
    terms by subtracting the change in price relative to prices n-periods
    ago.

    The default period is set to 12, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - Momentum(self.data, period=self.params.period)
        - Momentum(self.data, period=self.p.period)
        - Momentum(self.data, period=12)
        - Momentum(self.data)

    Formula:
    
        - data - data(-period)

    Additional information found at:
    https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    
    """

    lines = ('momentum', )
    params = (('period', 12), )

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(momentum=dict(_name='=', color='navy'))

    def __init__(self):
        self.lines.momentum = self.data - self.data(-self.params.period)

        super(Momentum, self).__init__()


class MomentumOscillator(Indicator):

    """Momentum Oscillator - measures the strength of a trend based on the
    ratio of the current price relative to the price n-periods ago, multiplied
    by 100 to change the scale. A value of 100 in this instance would signify
    par value between prices then and now.

    The default period is set to 12, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - MomentumOscillator(self.data, period=self.params.period)
        - MomentumOscillator(self.data, period=self.p.period)
        - MomentumOscillator(self.data, period=12)
        - MomentumOscillator(self.data)

    Formula:
    
        - 100 * (data / data(-period))

    Additional information found at:
    https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    
    """
 
    alias = ('MomentumOsc', )
    lines = ('momosc', )
    params = (('period', 12),
              ('band', 100.0))
    
    plotlines = dict(momosc=dict(_name='=', color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period]
        return plabels

    def _plotinit(self):
        self.plotinfo.plothlines = [self.params.band]

    def __init__(self):
        self.lines.momosc = 100.0 * (self.data / self.data(-self.params.period))

        super(MomentumOscillator, self).__init__()


class RateOfChange(Indicator):

    """Rate of Change - the change in price relative to itself n-periods ago,
    displayed in decimal format.
    
    The default period is set to 12, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - RateOfChange(self.data, period=self.params.period)
        - RateOfChange(self.data, period=self.p.period)
        - RateOfChange(self.data, period=12)
        - RateOfChange(self.data)

    Formula:
    
        - (data - data(-period)) / data(-period)

    Additional information found at:
    https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    
    """

    alias = ('ROC', )
    lines = ('roc', )
    params = (('period', 12), )

    plotlines = dict(roc=dict(_name='ROC =', color='navy'))

    def __init__(self):
        dperiod = self.data(-self.params.period)
        self.lines.roc = (self.data - dperiod) / dperiod

        super(RateOfChange, self).__init__()


class RateOfChange100(Indicator):

    """Rate of Change - the percentage change in price relative to itself
    n-periods ago.
    
    The default period is set to 12, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - RateOfChange100(self.data, period=self.params.period)
        - RateOfChange100(self.data, period=self.p.period)
        - RateOfChange100(self.data, period=12)
        - RateOfChange100(self.data)

    Formula:
    
        - 100 * (data - data(-period)) / data(-period)

    Additional information found at:
    https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    
    """

    alias = ('ROC100', )
    lines = ('roc100', )
    params = (('period', 12), )

    plotlines = dict(roc100=dict(_name='%ROC =', color='navy'))

    def __init__(self):
        self.lines.roc100 = 100.0 * RateOfChange(self.data, period=self.params.period)
        
        super(RateOfChange100, self).__init__()