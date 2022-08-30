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



class EnvelopeMixIn(object):
    
    """MixIn class to create a subclass with another indicator. The main output
    line of that indicator will be surrounded by an upper and a lower band, the
    distance of which is a given percentage relative to the input line.

    Usage is formatted as such:

        - Class xxxEnvelope(xxx, EnvelopeMixIn)

    Formula:

        - top = input * (1 + perc)
        - bottom = input * (1 - perc)

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/mae
    https://www.investopedia.com/articles/trading/08/moving-average-envelope.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_envelopes
    
    """

    lines = ('top', 'bottom')
    params = (('perc', 2.5), )

    plotlines = dict(top=dict(_samecolor=True), bottom=dict(_samecolor=True))

    def __init__(self):
        perc = self.params.perc / 100.0

        self.lines.top = self.lines[0] * (1.0 + perc)
        self.lines.bottom = self.lines[0] * (1.0 - perc)

        super(EnvelopeMixIn, self).__init__()


class _EnvelopeBase(Indicator):

    """Moving average envelope base class."""

    lines = ('src', )

    plotinfo = dict(subplot=False, plotlinevalues=False)
    plotlines = dict(src=dict(_plotskip=True))

    def __init__(self):
        self.lines.src = self.data

        super(_EnvelopeBase, self).__init__()


class Envelope(_EnvelopeBase, EnvelopeMixIn):

    """Moving Average Envelope - works in a similar way to Bollinger Bands and
    Keltner Channels by surrounding the moving average ouput line with upper
    and lower trading ranges. These ranges help to identify overbought and
    oversold prices.

    The default percentage for the envelope bands is set to 2.5%, but this can
    be overridden when calling the function.

    At a minimum, it requires a moving average type and a data feed. For
    example:

        - Envelope(SMA(self.data, period=self.params.period))
        - Envelope(EMA(self.data), perc=self.p.perc)
        - Envelope(WMA(self.data, period=50), perc=4)
        - Envelope(SMMA(self.data))

    Formula:

        - input = MovingAverage(data)
        - top = input * (1 + perc)
        - bottom = input * (1 - perc)

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/mae
    https://www.investopedia.com/articles/trading/08/moving-average-envelope.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_envelopes
    
    """


# Automatic creation of Moving Average Envelope classes

for movav in MovingAverage._movavs[1:]:
    _newclsdoc = """

    %s and envelope bands separated by "perc"

    Formula:

        - %s (from %s)
        - top = %s * (1 + perc)
        - botom = %s * (1 - perc)

    Additional information found at:
    https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_envelopes

    """
    
    # Skip aliases - they will be created automatically
    if getattr(movav, 'aliased', ''):
        continue

    movname = movav.__name__
    linename = movav.lines._getlinealias(0)
    newclsname = movname + 'Envelope'

    newaliases = []
    for alias in getattr(movav, 'alias', []):
        for suffix in ['Envelope']:
            newaliases.append(alias + suffix)

    newclsdoc = _newclsdoc % (movname, linename, movname, linename, linename)

    newclsdct = {'__doc__': newclsdoc,
                 '__module__': EnvelopeMixIn.__module__,
                 '_notregister': True,
                 'alias': newaliases}
    newcls = type(str(newclsname), (movav, EnvelopeMixIn), newclsdct)
    module = sys.modules[EnvelopeMixIn.__module__]
    setattr(module, newclsname, newcls)