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



class DetrendedPriceOscillator(Indicator):

    """Detrended Price Oscillator - attempts to eliminate the long-term trends
    in prices by using a displaced moving average to avoid reacting to the most
    recent changes in price. This allows the indicator to show intermediate
    overbought and oversold levels.

    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DetrendedPriceOscillator(self.data, period=self.params.period)
        - DetrendedPriceOscillator(self.data, period=self.p.period)
        - DetrendedPriceOscillator(self.data, period=20)
        - DetrendedPriceOscillator(self.data)

    Formula:

        - _movav = SMA(data, period)
        - DPO = data - _movav(-period / 2 + 1)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DetrendedPriceOscillator(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Detrended_price_oscillator
    https://www.investopedia.com/terms/d/detrended-price-oscillator-dpo.asp
    
    """

    alias = ('DPO', )
    lines = ('dpo', )
    params = (('period', 20), ('_movav', MovAv.Simple))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(dpo=dict(_name='DPO', color='navy'))

    def __init__(self):
        ma = self.params._movav(self.data, period=self.params.period)
        self.lines.dpo = self.data - ma(-self.params.period // 2 + 1)

        super(DetrendedPriceOscillator, self).__init__()