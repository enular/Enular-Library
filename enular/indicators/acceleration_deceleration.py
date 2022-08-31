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
from . import MovAv, AwesomeOscillator



class AccelerationDecelerationOscillator(Indicator):

    """Acceleration/Deceleration Oscillator - with regard to price movements,
    this indicator models the rate at which changes in momentum are acceleratory
    or deceleratory in nature.

    The default period is set to 5, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AccelerationDecelerationOscillator(self.data, period=self.params.period)
        - AccelerationDecelerationOscillator(self.data, period=self.p.period)
        - AccelerationDecelerationOscillator(self.data, period=5)
        - AccelerationDecelerationOscillator(self.data)

    Formula:
    
        - AwesomeOscillator - SMA(AwesomeOscillator, period)

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - AccelerationDecelerationOscillator(self.data, _movav=WMA)

    Additional information found at:
    https://admiralmarkets.com/education/articles/forex-indicators/accelerator-oscillator
    https://www.metatrader5.com/en/terminal/help/indicators/bw_indicators/ao
    
    """

    alias = ('AccDeOsc', )
    lines = ('accdec', )
    params = (('period', 5), ('_movav', MovAv.SMA))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(accdec=dict(_name='=',
                                 _method='bar',
                                 color='white',
                                 _fill_gt=(0, ('forestgreen', 0.7)),
                                 _fill_lt=(0, ('crimson', 0.7)),
                                 width=1.0))

    def __init__(self):
        ao = AwesomeOscillator(self.data)
        self.lines.accdec = ao - self.params._movav(ao,
                                                    period=self.params.period)

        super(AccelerationDecelerationOscillator, self).__init__()