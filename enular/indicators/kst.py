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
from . import MovAv, ROC100



class KnowSureThing(Indicator):

    """Know Sure Thing - a momentum indicator based on the smoothed
    rate-of-change across four timeframes, combining them into one oscillator.
    It is used to identify divergences, signal-line crossovers, centreline
    crossovers, and sometimes trends.

    This indicator requires 10 positional arguments that can be overridden when
    calling the function. The default values are:

        - rp1, rma1 = 10, 10
        - rp2, rma2 = 15, 10
        - rp3, rma3 = 20, 10
        - rp4, rma4 = 30, 10
        - rsignal = 9
        - rfactors = [1.0, 2.0, 3.0, 4.0] # must be entered in list format

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - KnowSureThing(self.data, rp1=self.params.rp1, rma1=self.params.rma1)
        - KnowSureThing(self.data, rp1=self.p.rp1, rma1=self.p.rma1)
        - KnowSureThing(self.data, rp1=10, rma1=10, rp2=10, rma2=15)
        - KnowSureThing(self.data)

    Formula:

        - rcma1 = _rmovav(roc100(rp1), rma1)
        - rcma2 = _rmovav(roc100(rp2), rma2)
        - rcma3 = _rmovav(roc100(rp3), rma3)
        - rcma4 = _rmovav(roc100(rp4), rma4)
        - kst = 1.0 * rcma1 + 2.0 * rcma2 + 3.0 * rcma3 + 4.0 * rcma4
        - signal = _smovav(kst, rsignal)

    Notes:

        - Although the standard moving averages used are SMAs, these can be
          switched to any other. For example, use WMA and EMA by including
          _rmovav=WMA and _smovav=EMA in the function.
        - KnowSureThing(self.data, _rmovav=WMA, _smovav=EMA)

    Additional information found at:
    https://school.stockcharts.com/doku.php?id=technical_indicators:know_sure_thing_kst
    https://www.investopedia.com/terms/k/know-sure-thing-kst.asp
    
    """

    alias = ('KST', )
    lines = ('kst', 'signal')
    params = (('rp1', 10), ('rp2', 15), ('rp3', 20), ('rp4', 30),
              ('rma1', 10), ('rma2', 10), ('rma3', 10), ('rma4', 10),
              ('rsignal', 9),
              ('rfactors', [1.0, 2.0, 3.0, 4.0]),
              ('_rmovav', MovAv.Simple),
              ('_smovav', MovAv.Simple))

    plotinfo = dict(plothlines=[0.0])
    plotlines = dict(kst=dict(color='crimson'),
                     signal=dict(ls='--', color='navy'))

    def _plotlabel(self):
        plabels = [self.params._rmovav, self.params._smovav]
        return plabels

    def __init__(self):
        rcma1 = self.params._rmovav(ROC100(period=self.params.rp1), period=self.params.rma1)
        rcma2 = self.params._rmovav(ROC100(period=self.params.rp2), period=self.params.rma2)
        rcma3 = self.params._rmovav(ROC100(period=self.params.rp3), period=self.params.rma3)
        rcma4 = self.params._rmovav(ROC100(period=self.params.rp4), period=self.params.rma4)
        
        self.lines.kst = sum([rfi * rci for rfi, rci in
                                zip(self.params.rfactors, [rcma1, rcma2, rcma3, rcma4])])

        self.lines.signal = self.params._smovav(self.lines.kst, period=self.params.rsignal)

        super(KnowSureThing, self).__init__()