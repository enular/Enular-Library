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
from . import MovAv, MeanDev



class CommodityChannelIndex(Indicator):

    """Commodity Channel Index - a momentum based indicator that measures the
    variation in price from its statistical mean, helping to identify whether
    an asset is reaching a condition of being overbought or oversold.

    This indicator requires two positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 20
        - factor = 0.015

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - CommodityChannelIndex(self.data, period=self.params.period)
        - CommodityChannelIndex(self.data, period=self.p.period, factor=self.p.factor)
        - CommodityChannelIndex(self.data, period=20, factor=0.015)
        - CommodityChannelIndex(self.data)

    Formula:
    
        - typical price = (high + low + close) / 3
        - mean = SMA(typical price, period)
        - deviation = typical price - mean
        - CCI = deviation / (MeanDeviation(mean) * factor)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - CommodityChannelIndex(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Commodity_channel_index
    https://www.investopedia.com/terms/c/commoditychannelindex.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:commodity_channel_index_cci
    
    """

    alias = ('CCI', )
    lines = ('cci', )
    params = (('period', 20),
              ('factor', 0.015),
              ('_movav', MovAv.Simple),
              ('upperband', 100.0),
              ('lowerband', -100.0))
    
    plotlines = dict(cci=dict(color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period, self.params.factor, self.params._movav]
        return plabels

    def _plotinit(self):
        self.plotinfo.plotyhlines = [0.0,
                                     self.params.upperband,
                                     self.params.lowerband]

    def __init__(self):
        tp = (self.data.high + self.data.low + self.data.close) / 3.0
        tpmean = self.params._movav(tp, period=self.params.period)

        dev = tp - tpmean
        meandev = MeanDev(tp, tpmean, period=self.params.period)

        self.lines.cci = dev / (self.params.factor * meandev)

        super(CommodityChannelIndex, self).__init__()