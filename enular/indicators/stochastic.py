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

from . import Indicator, Max, MovAv, Highest, Lowest, DivByZero



class _StochasticBase(Indicator):

    """Base class for stochastic indicators."""

    lines = ('percK', 'percD', )
    params = (('period', 14), ('period_dfast', 3), ('_movav', MovAv.Simple),
              ('upperband', 80.0), ('lowerband', 20.0),
              ('safediv', False), ('safezero', 0.0))

    plotlines = dict(percD=dict(_name='%D', color='navy', ls='--'),
                     percK=dict(_name='%K', color='crimson'))

    def _plotlabel(self):
        plabels = [self.params.period, self.params.period_dfast]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        return plabels

    def _plotinit(self):
        self.plotinfo.plotyhlines = [self.params.upperband, self.params.lowerband]

    def __init__(self):
        highesthigh = Highest(self.data.high, period=self.params.period)
        lowestlow = Lowest(self.data.low, period=self.params.period)
        knum = self.data.close - lowestlow
        kden = highesthigh - lowestlow
        if self.params.safediv:
            self.k = 100.0 * DivByZero(knum, kden, zero=self.params.safezero)
        else:
            self.k = 100.0 * (knum / kden)
        self.d = self.params._movav(self.k, period=self.params.period_dfast)

        super(_StochasticBase, self).__init__()


class StochasticFast(_StochasticBase):

    """Fast Stochastic Oscillator - aims to predict price turning points by
    comparing the current price to the price range over a given period. This
    indicator is the fast version that does not contain a smoothing component
    on the %K line.

    This indicator requires two positional arguments that can be overridden when
    calling the function. The default values are:

        - period = 14
        - period_dfast = 3

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - StochasticFast(self.data, period=self.params.period)
        - StochasticFast(self.data, period=self.p.period, period_dfast=self.p.period_dfast)
        - StochasticFast(self.data, period=14, period_dfast=3)
        - StochasticFast(self.data)

    Formula:

        - hh = highest(data.high, period)
        - ll = lowest(data.low, period)
        - knum = data.close - ll
        - kden = hh - ll
        - k = 100 * (knum / kden)
        - d = MovingAverage(k, period_dfast)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - StochasticFast(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/s/stochasticoscillator.asp
    https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/fast-stochastic-indicator/
    https://en.wikipedia.org/wiki/Stochastic_oscillator
    
    """

    def __init__(self):
        super(StochasticFast, self).__init__()

        self.lines.percK = self.k
        self.lines.percD = self.d


class Stochastic(_StochasticBase):

    """Slow Stochastic Oscillator - aims to predict price turning points by
    comparing the current price to the price range over a given period. This
    indicator is the slow (or regular) version where the percD line of the Fast
    Stochastic becomes the percK line, and the percD line becomes a moving
    average of the original percD.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 14
        - period_dfast = 3
        - period_dslow = 3

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - Stochastic(self.data, period=self.params.period)
        - Stochastic(self.data, period=self.p.period, period_dfast=self.p.period_dfast)
        - Stochastic(self.data, period=14, period_dfast=3, period_dslow=3)
        - Stochastic(self.data)

    Formula:

        - hh = highest(data.high, period)
        - ll = lowest(data.low, period)
        - knum = data.close - ll
        - kden = hh - ll
        - k = 100 * (knum / kden)
        - d = MovingAverage(k, period_dfast)
        - k_slow = d
        - d_slow = MovingAverage(d, period_dslow)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - Stochastic(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/s/stochasticoscillator.asp
    https://en.wikipedia.org/wiki/Stochastic_oscillator
    
    """

    alias = ('StochasticSlow', )
    params = (('period_dslow', 3), )

    def _plotlabel(self):
        plabels = [self.params.period, self.params.period_dfast, self.params.period_dslow]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        return plabels

    def __init__(self):
        super(Stochastic, self).__init__()

        self.lines.percK = self.d
        self.lines.percD = self.params._movav(self.lines.percK, period=self.params.period_dslow)


class StochasticFull(_StochasticBase):

    """Full Stochastic Oscillator - aims to predict price turning points by
    comparing the current price to the price range over a given period. This
    indicator is the full version that includes the orginal output of the Fast
    Stochastic with the additional slowed percD line.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 14
        - period_dfast = 3
        - period_dslow = 3

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - StochasticFull(self.data, period=self.params.period)
        - StochasticFull(self.data, period=self.p.period, period_dfast=self.p.period_dfast)
        - StochasticFull(self.data, period=14, period_dfast=3, period_dslow=3)
        - StochasticFull(self.data)

    Formula:

        - hh = highest(data.high, period)
        - ll = lowest(data.low, period)
        - knum = data.close - ll
        - kden = hh - ll
        - k = 100 * (knum / kden)
        - d = MovingAverage(k, period_dfast)
        - d_slow = MovingAverage(d, period_dslow)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - StochasticFull(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/s/stochasticoscillator.asp
    https://en.wikipedia.org/wiki/Stochastic_oscillator
    
    """

    lines = ('percDSlow', )
    params = (('period_dslow', 3), )

    plotlines = dict(percDSlow=dict(_name='%DSlow', color='forestgreen'))

    def _plotlabel(self):
        plabels = [self.params.period, self.params.period_dfast, self.params.period_dslow]
        plabels += [self.params._movav] * self.params.notdefault('_movav')
        return plabels

    def __init__(self):
        super(StochasticFull, self).__init__()
        
        self.lines.percK = self.k
        self.lines.percD = self.d
        self.lines.percDSlow = self.params._movav(self.lines.percD,
                                                  period=self.params.period_dslow)