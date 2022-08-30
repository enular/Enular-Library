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

from . import RSI



class RelativeMomentumIndex(RSI):

    """Relative Momentum Index - while the standard RSI counts up and down days
    from close to close, the RMI counts up and down days from the close relative
    to a close n-periods ago, producing a smoother version of the RSI.

    This indicator requires two positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 20
        - lookback = 5

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - RelativeMomentumIndex(self.data, period=self.params.period)
        - RelativeMomentumIndex(self.data, period=self.p.period, lookback=self.p.lookback)
        - RelativeMomentumIndex(self.data, period=20, lookback=5)
        - RelativeMomentumIndex(self.data)

    Additional information found at:
    https://www.marketvolume.com/technicalanalysis/relativemomentumindex.asp
    https://www.tradingview.com/script/UCm7fIvk-FREE-INDICATOR-Relative-Momentum-Index-RMI/
    https://www.prorealcode.com/prorealtime-indicators/relative-momentum-index-rmi/
    
    """

    alias = ('RMI', )
    linealias = (('rsi', 'rmi'), )
    plotlines = dict(rsi=dict(_name='rmi'))

    params = (('period', 20), ('lookback', 5))

    def _plotlabel(self):
        # override to always print the lookback label and do it before movav
        plabels = [self.params.period]
        plabels += [self.params.lookback]
        plabels += [self.params.movav] * self.params.notdefault('movav')
        return plabels