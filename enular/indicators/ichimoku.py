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

from . import Indicator, Highest, Lowest



class Ichimoku(Indicator):

    """Ichimoku Cloud - displays support and resistance levels, as well as trend
    and momentum. When the shorter term Tenkan Sen line rises above the longer
    term Kijun Sen line, the trend is typically positive. And when the opposite
    happens, when the Tenkan Sen falls below the Kijun Sen, the trend is
    typically negative. Both are then analysed in relationship to the Cloud,
    which is composed of the area between Senkou A and B and helps to identify
    the strength of the trend in addition to the direction.

    This indicator requires 5 positional arguments that can be overridden when
    calling the function. The default values are:

        - tenkan = 9
        - kijun = 26
        - senkou = 52
        - senkou_lead = 26
        - chikou = 26

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - Ichimoku(self.data, tenkan=self.params.tenkan)
        - Ichimoku(self.data, tenkan=self.p.tenkan, kijun=self.p.kijun)
        - Ichimoku(self.data, tenkan=9, kijun=26, senkou=52)
        - Ichimoku(self.data)

    Formula:

        - tenkan_sen = (Highest(data.high, tenkan) + Lowest(data.low, tenkan)) / 2
        - kijun_sen = (Highest(data.high, kijun) + Lowest(data.low, kijun)) / 2
        - senkou_span_a = (tenkan_sen + kijun_sen) / 2
        - senkou_span_b = (Highest(data.high, senkou) + Lowest(data.low, senkou)) / 2
        - chikou = data.close(chikou period)

    Additional information found at:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/Ichimoku-Cloud
    https://school.stockcharts.com/doku.php?id=technical_indicators:ichimoku_cloud
    https://www.investopedia.com/terms/i/ichimoku-cloud.asp
        
    """
    
    lines = ('tenkan_sen', 'kijun_sen',
             'senkou_span_a', 'senkou_span_b', 'chikou_span')

    params = (('tenkan', 9),
              ('kijun', 26),
              ('senkou', 52),
              ('senkou_lead', 26),  # forward push
              ('chikou', 26))  # backwards push

    plotinfo = dict(subplot=False, plotlinevalues=False)

    plotlines = dict(tenkan_sen=dict(color='darkgoldenrod', alpha=0.3),
                     kijun_sen=dict(color='blue', alpha=0.3),
                     chikou_span=dict(color='mediumvioletred', alpha=0.3),
                     senkou_span_a=dict(color='forestgreen',
                                        alpha=0.3,
                                        _fill_gt=('senkou_span_b', ('forestgreen', 0.7)),
                                        _fill_lt=('senkou_span_b', ('crimson', 0.7))),
                     senkou_span_b=dict(color='crimson', alpha=0.3))

    def __init__(self):
        hi_tenkan = Highest(self.data.high, period=self.params.tenkan)
        lo_tenkan = Lowest(self.data.low, period=self.params.tenkan)
        self.lines.tenkan_sen = (hi_tenkan + lo_tenkan) / 2.0

        hi_kijun = Highest(self.data.high, period=self.params.kijun)
        lo_kijun = Lowest(self.data.low, period=self.params.kijun)
        self.lines.kijun_sen = (hi_kijun + lo_kijun) / 2.0

        senkou_span_a = (self.lines.tenkan_sen + self.lines.kijun_sen) / 2.0
        self.lines.senkou_span_a = senkou_span_a(-self.params.senkou_lead)

        hi_senkou = Highest(self.data.high, period=self.params.senkou)
        lo_senkou = Lowest(self.data.low, period=self.params.senkou)
        senkou_span_b = (hi_senkou + lo_senkou) / 2.0
        self.lines.senkou_span_b = senkou_span_b(-self.params.senkou_lead)

        self.lines.chikou_span = self.data.close(self.params.chikou)

        super(Ichimoku, self).__init__()