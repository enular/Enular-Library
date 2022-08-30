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
                        
from . import Indicator, FindFirstIndexHighest, FindFirstIndexLowest



class _AroonBase(Indicator):

    """Base class to calculate AroonUp/AroonDown values and define common
    parameters.

    Uses the class attributes _up and _down (Boolean flags) to decide which
    value should be calculated.
    
    Values are not assigned to lines, rather they are stored in the 'up' and
    'down' instance variables which can be used by subclasses for assignment
    or further calculations.

    """

    _up = False
    _down = False

    params = (('period', 14),
              ('upperband', 70),
              ('lowerband', 30))

    plotinfo = dict(plotymargin=0.05, plotyhlines=[0, 100])

    def _plotlabel(self):
        plabels = [self.params.period]
        return plabels

    def _plotinit(self):
        self.plotinfo.plotyhlines += [self.params.lowerband, self.params.upperband]

    def __init__(self):
        # Look backwards period + 1 for current data as the formula must
        # produce values between 0 and 100 and can only do that if the
        # calculated hhidx/llidx go from 0 to period (hence period + 1 values)
        idxperiod = self.params.period + 1

        if self._up:
            hhidx = FindFirstIndexHighest(self.data.high, period=idxperiod)
            self.up = (100.0 / self.params.period) * (self.params.period - hhidx)

        if self._down:
            llidx = FindFirstIndexLowest(self.data.low, period=idxperiod)
            self.down = (100.0 / self.params.period) * (self.params.period - llidx)

        super(_AroonBase, self).__init__()


class AroonUp(_AroonBase):

    """AroonUp - measures the time since prices have recorded a new high within
    the specified period. If the current bar's high is the highest within the
    user defined number of periods before it, then the AroonUp value is 100.
    Therefore, this represents a new high for that period. Otherwise, it returns
    a percent value indicating the time since a new high occurred for the
    specified period.

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AroonUp(self.data, period=self.params.period)
        - AroonUp(self.data, period=self.p.period)
        - AroonUp(self.data, period=14)
        - AroonUp(self.data)

    Formula:

        - up = 100 * (period - distance to highest high) / period

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator
    https://www.investopedia.com/terms/a/aroon.asp

    """

    _up = True

    lines = ('aroonup', )

    plotlines = dict(aroonup=dict(color='crimson'))

    def __init__(self):
        super(AroonUp, self).__init__()

        self.lines.aroonup = self.up


class AroonDown(_AroonBase):

    """AroonDown - measures the time since prices have recorded a new low within
    the specified period. If the current bar's low is the lowest within the user
    defined number of periods before it, then the AroonDown value is 100.
    Therefore, this represents a new low for that period. Otherwise, it returns
    a percent value indicating the time since the new low occurred for the
    specified period.

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AroonDown(self.data, period=self.params.period)
        - AroonDown(self.data, period=self.p.period)
        - AroonDown(self.data, period=14)
        - AroonDown(self.data)

    Formula:

        - down = 100 * (period - distance to lowest low) / period

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator
    https://www.investopedia.com/terms/a/aroon.asp
    
    """
 
    _down = True

    lines = ('aroondown', )
    
    plotlines = dict(aroondown=dict(color='navy'))

    def __init__(self):
        super(AroonDown, self).__init__()

        self.lines.aroondown = self.down


class AroonUpDown(AroonUp, AroonDown):

    """Aroon Up/Down indicator - developed by Tushar Chande in 1995, indicates
    if a price is trending or is in a trading range. Furthermore, it may also
    reveal the beginning of a new trend, its strength, and can help anticipate
    changes from trading ranges to trends.

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AroonUpDown(self.data, period=self.params.period)
        - AroonUpDown(self.data, period=self.p.period)
        - AroonUpDown(self.data, period=14)
        - AroonUpDown(self.data)

    Formula:

        - up = 100 * (period - distance to highest high) / period
        - down = 100 * (period - distance to lowest low) / period

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator
    https://www.investopedia.com/terms/a/aroon.asp
    
    """

    alias = ('AroonIndicator', )


class AroonOscillator(_AroonBase):

    """Aroon Oscillator - a variation of the AroonUpDown indicator which shows
    the difference between the AroonUp and AroonDown values to gauge the
    strength of a current trend and the likelihood that it will continue.

    Aroon Oscillator values above zero indicate that an uptrend is present,
    whereas readings below zero indicate that a downtrend is present.

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AroonOscillator(self.data, period=self.params.period)
        - AroonOscillator(self.data, period=self.p.period)
        - AroonOscillator(self.data, period=14)
        - AroonOscillator(self.data)
    
    Formula:

        - AroonOscillator = AroonUp - AroonDown

    Additional information found at:
    https://www.investopedia.com/terms/a/aroonoscillator.asp
    
    """

    _up = True
    _down = True

    alias = ('AroonOsc', )
    lines = ('aroonosc', )

    plotlines = dict(aroonosc=dict(color='forestgreen'))

    def _plotinit(self):
        super(AroonOscillator, self)._plotinit()

        for yhline in self.plotinfo.plotyhlines[:]:
            self.plotinfo.plotyhlines.append(-yhline)

    def __init__(self):
        super(AroonOscillator, self).__init__()

        self.lines.aroonosc = self.up - self.down


class AroonUpDownOscillator(AroonUpDown, AroonOscillator):

    """Aroon Up/Down Oscillator - presents the AroonUpDown and the
    AroonOscillator indicators together.

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AroonUpDownOscillator(self.data, period=self.params.period)
        - AroonUpDownOscillator(self.data, period=self.p.period)
        - AroonUpDownOscillator(self.data, period=14)
        - AroonUpDownOscillator(self.data)

    Additional information found at:

    https://www.investopedia.com/terms/a/aroonoscillator.asp
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator
    https://www.investopedia.com/terms/a/aroon.asp
    
    """

    alias = ('AroonUpDownOsc', )