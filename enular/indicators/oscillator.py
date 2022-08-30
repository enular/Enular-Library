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

import sys

from . import Indicator, MovingAverage



class OscillatorMixIn(Indicator):

    """MixIn class to create a subclass with another indicator. The main line of
    that indicator will be substracted from the other base class's main line to
    create an oscillator.

    Usage is formatted as such:

        - Class xxxOscillator(xxx, OscillatorMixIn)

    Formula:

        - xxx calculates lines[0]
        - osc = self.data - xxx.lines[0]

    Additional information found at:
    https://en.wikipedia.org/wiki/Oscillator_(technical_analysis)
    https://www.investopedia.com/terms/o/oscillator.asp
    
    """

    plotlines = dict(_0=dict(_name='osc'))

    def _plotinit(self):
        try:
            lname = self.lines._getlinealias(0)
            self.plotlines._0._name = lname + '_osc'
        except AttributeError:
            pass

    def __init__(self):
        self.lines[0] = self.data - self.lines[0]
        super(OscillatorMixIn, self).__init__()


class Oscillator(Indicator):

    """Creates the oscillation of a given data around another. This indicator
    can accept one or two data sets for the calculation. If one is provided, it
    must be a complex 'lines' object (indicator) with a data feed, e.g. a moving
    average. The calculated oscillation will be that of the moving average (in
    this example) around the raw data that was used for the input. If two data
    sources are provided, the calculated oscillation will be that of the second
    data source around the first.

    At a minimum, it requires a lines object and a data feed. For example:

        - Oscillator(SMA(self.data, period=self.params.period))
        - Oscillator(WMA(self.data, period=50))
        - Oscillator(EMA(self.data), DMA(self.data))

    Formula:

        - one data source --> osc = data.data - data
        - two data sources --> osc = data0 - data1

    Additional information found at:
    https://en.wikipedia.org/wiki/Oscillator_(technical_analysis)
    https://www.investopedia.com/terms/o/oscillator.asp
    
    """

    lines = ('osc', )

    plotlines = dict(_0=dict(_name='osc'))

    def _plotinit(self):
        try:
            lname = self.dataosc._getlinealias(0)
            self.plotlines._0._name = lname + '_osc'
        except AttributeError:
            pass

    def __init__(self):
        super(Oscillator, self).__init__()

        if len(self.datas) > 1:
            datasrc = self.data
            self.dataosc = self.data1
        else:
            datasrc = self.data.data
            self.dataosc = self.data

        self.lines[0] = datasrc - self.dataosc


# Automatic creation of oscillating lines

for movav in MovingAverage._movavs[1:]:
    _newclsdoc = """
    Oscillation of a %s around its data
    """
    # Skip aliases - they will be created automatically
    if getattr(movav, 'aliased', ''):
        continue

    movname = movav.__name__
    linename = movav.lines._getlinealias(0)
    newclsname = movname + 'Oscillator'

    newaliases = [movname + 'Osc']
    for alias in getattr(movav, 'alias', []):
        for suffix in ['Oscillator', 'Osc']:
            newaliases.append(alias + suffix)

    newclsdoc = _newclsdoc % movname
    newclsdct = {'__doc__': newclsdoc,
                 '__module__': OscillatorMixIn.__module__,
                 '_notregister': True,
                 'alias': newaliases}

    newcls = type(str(newclsname), (movav, OscillatorMixIn), newclsdct)
    module = sys.modules[OscillatorMixIn.__module__]
    setattr(module, newclsname, newcls)