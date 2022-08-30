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

from . import Indicator, Max, MovAv



class _PriceOscBase(Indicator):

    """Price Oscillator base class."""

    params = (('period1', 12),
              ('period2', 26),
              ('_movav', MovAv.Exponential))

    plotinfo = dict(plothlines=[0.0])

    def __init__(self):
        self.ma1 = self.params._movav(self.data, period=self.params.period1)
        self.ma2 = self.params._movav(self.data, period=self.params.period2)
        self.lines[0] = self.ma1 - self.ma2

        super(_PriceOscBase, self).__init__()


class PriceOscillator(_PriceOscBase):

    """Price Oscillator - returns the difference between a short and long
    exponential moving average, expressed in points.

    This indicator requires two positional arguments that can be overridden
    when calling the function. The default values are:

        - period1 = 12
        - period2 = 26

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - PriceOscillator(self.data, period1=self.params.period1)
        - PriceOscillator(self.data, period1=self.p.m1_period1, period2=self.p.period2)
        - PriceOscillator(self.data, period1=12, period2=26)
        - PriceOscillator(self.data)

    Formula:

        - PO = EMA(short period) - EMA(long period)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - PriceOscillator(self.data, _movav=WMA)

    Additional information found at:
    https://www.tradingview.com/scripts/priceoscillator/
    https://www.metastock.com/Customer/Resources/TAAZ/?c=3&p=94
    
    """

    alias = ('PriceOsc', 'AbsolutePriceOscillator', 'APO', 'AbsPriceOsc')
    lines = ('po', )

    plotlines = dict(po=dict(color='navy'))


class PercentagePriceOscillator(_PriceOscBase):

    """Percentage Price Oscillator - returns the difference between a short and
    long exponential moving average, expressed as a percentage. Works similar
    to MACD.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period1 = 12
        - period2 = 26
        - period_signal = 9

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - PercentagePriceOscillator(self.data, period1=self.params.period1)
        - PercentagePriceOscillator(self.data, period1=self.p.m1_period1, period2=self.p.period2)
        - PercentagePriceOscillator(self.data, period1=12, period2=26, period_signal=9)
        - PercentagePriceOscillator(self.data)

    Formula:

        - PPO = 100 * (EMA(short period) - EMA(long period)) / EMA(long period)
        - signal = EMA(ppo, signal period)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - PercentagePriceOscillator(self.data, _movav=WMA)

    Additional information found at:
    https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo
    https://www.investopedia.com/terms/p/ppo.asp
    
    """

    _long = True

    alias = ('PPO', 'PercPriceOsc')
    lines = ('ppo', 'signal', 'histo')
    params = (('period_signal', 9), )

    plotlines = dict(ppo=dict(color='crimson'), 
                     signal=dict(ls='--', color='navy'),
                     histo=dict(_method='bar',
                                color='forestgreen',
                                alpha=0.5,
                                width=1.0))

    def __init__(self):
        super(PercentagePriceOscillator, self).__init__()

        den = self.ma2 if self._long else self.ma1

        self.lines.ppo = 100.0 * self.lines[0] / den
        self.lines.signal = self.params._movav(self.lines.ppo, period=self.params.period_signal)
        self.lines.histo = self.lines.ppo - self.lines.signal


class PercentagePriceOscillatorShort(PercentagePriceOscillator):

    """Percentage Price Oscillator (short) - returns the difference between a
    short and long exponential moving average, expressed as a percentage. Works
    similar to MACD.

    This variation uses the short EMA period in the denominator of the fuction.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period1 = 12
        - period2 = 26
        - period_signal = 9

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - PercentagePriceOscillatorShort(self.data, period1=self.params.period1)
        - PercentagePriceOscillatorShort(self.data, period1=self.p.m1_period1, period2=self.p.period2)
        - PercentagePriceOscillatorShort(self.data, period1=12, period2=26, period_signal=9)
        - PercentagePriceOscillatorShort(self.data)

    Formula:

        - PPO = 100 * (EMA(short period) - EMA(long period)) / EMA(short period)
        - signal = EMA(ppo, signal period)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - PercentagePriceOscillatorShort(self.data, _movav=WMA)

    Additional information found at:
    https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo
    https://www.investopedia.com/terms/p/ppo.asp
    
    """

    _long = False
    alias = ('PPOShort', 'PercPriceOscShort')