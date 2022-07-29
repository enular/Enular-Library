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
from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import enular

class SMA(enular.IndicatorOperation):

    """
    Simple Moving Average - calculates the average price over 'n' periods.
    
    The default period is set to 50, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    SMA(self.data, period=self.params.period)
    SMA(self.data, period=self.p.period)
    SMA(self.data, period=50)
    SMA(self.data)

    Formula: sum(data, period) / (period)

    Additional information found at:
    https://www.investopedia.com/terms/s/sma.asp
    https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average

    """

    lines = ('sma', )
    params = (('period', 50), )

    # plots the output over the price graph
    plotinfo = dict(subplot=False)
    plotlines = dict(sma=dict(color='blue'))

    def __init__(self):
        # the following function is located within Backtrader's basicops.py module
        self.lines.sma = bt.ind.Average(self.data, period=self.params.period)

class EMA(bt.Indicator):

    """
    Exponential Moving Average - applies a weighting factor
    to each data point in the moving average sum, favouring
    the most recent. The weighting of all subsequent data
    points decreases exponentially, never reaching zero.

    The default period is set to 20, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    EMA(self.data, period=self.params.period)
    EMA(self.data, period=self.p.period)
    EMA(self.data, period=20)
    EMA(self.data)
    
    Formula: data[0] * (smoothing factor / (1 + period))
             + EMA[-1] * (1 - (smoothing factor / 1 + period))
    
    Additional information found at:
    https://www.investopedia.com/terms/e/ema.asp
    https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    
    """

    lines = ('ema', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(ema=dict(color='blue'))

    def __init__(self):
        # the following function is located within Backtrader's basicops.py module
        self.lines.ema = bt.ind.ExponentialSmoothing(self.data,
                                            period=self.params.period,
                                            alpha=2.0 / (1.0 + self.params.period))
                                            # alpha (smoothing factor)

class DoubleEMA(bt.Indicator):

    """
    Double Exponential Moving Average - attempts to reduce the lag
    associated with with moving averages by applying additional
    weight on recent data points. This is not achieved by doubling
    the smoothing factor, rather, by subtracting a second order EMA
    from the doubled EMA.
    
    The default period is set to 20, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    DoubleEMA(self.data, period=self.params.period)
    DoubleEMA(self.data, period=self.p.period)
    DoubleEMA(self.data, period=20)
    DoubleEMA(self.data)

    Formula: 2*EMA - EMA(EMA)

    Additional information found at:
    https://www.investopedia.com/terms/d/double-exponential-moving-average.asp
    https://en.wikipedia.org/wiki/Double_exponential_moving_average
    
    """

    lines = ('double_ema', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(double_ema=dict(color='blue'))

    def __init__(self):
        ema1 = EMA(self.data, period=self.params.period)
        ema2 = EMA(ema1, period=self.params.period)

        self.lines.double_ema = 2.0 * ema1 - ema2

class TripleEMA(bt.Indicator):

    """
    Triple Exponential Moving Average - attempts to reduce the lag
    associated with with moving averages by applying additional
    weight on recent data points. This is not achieved by tripling
    the smoothing factor, rather, by subtracting a second order EMA
    3 times from the tripled EMA before adding a 3rd order EMA.

    The default period is set to 20, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    TripleEMA(self.data, period=self.params.period)
    TripleEMA(self.data, period=self.p.period)
    TripleEMA(self.data, period=20)
    TripleEMA(self.data)

    Formula: 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))

    Additional information found at:
    https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
    https://en.wikipedia.org/wiki/Triple_exponential_moving_average
    
    """

    lines = ('triple_ema', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(triple_ema=dict(color='blue'))

    def __init__(self):
        ema1 = EMA(self.data, period=self.params.period)
        ema2 = EMA(ema1, period=self.params.period)
        ema3 = EMA(ema2, period=self.params.period)

        self.lines.triple_ema = 3.0 * ema1 - 3.0 * ema2 + ema3

class WMA(bt.Indicator):

    """
    Weighted Moving Average - applies a fixed weighting to the
    moving average, greatest at the most recent data point, 
    decreasing arithmetically as the data points progress.

    The default period is set to 20, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    WMA(self.data, period=self.params.period)
    WMA(self.data, period=self.p.period)
    WMA(self.data, period=20)
    WMA(self.data)

    Formula: weighting coefficient * sum(weight[i] * data[period - i] for i in range(period))

    Additional information found at:
    https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average
    
    """

    lines = ('wma', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(wma=dict(color='blue'))

    def __init__(self):
        # calculation for the weighting coefficient
        coef = 2.0 / (self.params.period * (self.params.period + 1.0))

        # weights for the look-back period
        weights = tuple(float(x) for x in range(1, self.params.period + 1))

        # the following function is located within Backtrader's basicops.py module
        self.lines.wma = bt.ind.AverageWeighted(self.data,
                                                period=self.params.period,
                                                coef=coef,
                                                weights=weights)

class HMA(bt.Indicator):

    """
    Hull Moving Average - derived from the weighted moving average
    with the objective of further reducing lag and improving
    smoothness.
    
    The default period is set to 16, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    HMA(self.data, period=self.params.period)
    HMA(self.data, period=self.p.period)
    HMA(self.data, period=16)
    HMA(self.data)

    Formula: WMA(2 * WMA(period // 2) - WMA(period), sqrt(period))

    Additional information found at:
    https://alanhull.com/hull-moving-average
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/hull-moving-average
    https://school.stockcharts.com/doku.php?id=technical_indicators:hull_moving_average
    
    """

    lines = ('hma', )
    params = (('period', 16), )

    plotinfo = dict(subplot=False)
    plotlines = dict(hma=dict(color='blue'))

    def __init__(self):
        # first and second WMA values
        wma = WMA(self.data, period=self.params.period)
        wma2 = 2.0 * WMA(self.data, period=self.params.period // 2)

        sqrtperiod = pow(self.params.period, 0.5)

        self.lines.hma = WMA(wma2 - wma, period=int(sqrtperiod))

class DMA(bt.Indicator):

    """
    Dickson Moving Average - attempts to replicate the accuracy of
    a technique known as the Jurik Moving Average by combining the
    Zero Lag Indicator with the Hull Moving Average.

    This indicator requires 3 positional arguments that can be
    overridden when calling the function. The default values are:

        - period = 20
        - gainlimit = 50
        - hull_period = 7

    Calling the function requires 1 mandatory parameter, 'data,'
    with the additional optional parameters above. Examples:

    DMA(self.data, period=self.params.period)
    DMA(self.data, period=self.p.period, gainlimit=self.p.gainlimit, hull_period=self.p.hull_period)
    DMA(self.data, period=20, gainlimit=50, hull_period=7)
    DMA(self.data)

    Formula: (ZeroLagIndicator(period, gainlimit) + HMA(hull_period)) / 2

    Additional information found at:
    https://www.reddit.com/r/algotrading/comments/4xj3vh/dickson_moving_average
    
    """

    lines = ('dma', )
    params = (('period', 20),
              ('gainlimit', 50),
              ('hull_period', 7), )

    plotinfo = dict(subplot=False)
    plotlines = dict(dma=dict(color='blue'))

    def __init__(self):
        # error correcting component
        # the following function is located within Backtrader's basicops.py module
        ec = bt.ind.ZeroLagIndicator(period=self.params.period,
                                     gainlimit=self.params.gainlimit,
                                     _movav=EMA)

        # Hull component with reduced look-back period
        hull = HMA(period=self.params.hull_period)

        self.lines.dma = (ec + hull) / 2.0

class KAMA(bt.Indicator):

    """
    Kaufman's Adaptive Moving Average - uses a fast and slow
    exponential smoothing component to filter out market noise
    whilst accounting for price and volatility.

    The speed of the indicator quickly adapts to new trends and
    is best utilised in a trending environment, as opposed to
    stagnant markets.

    This indicator requires 3 positional arguments that can be
    overridden when calling the function. The default values are:

        - period = 10
        - fast = 2
        - slow = 30

    Calling the function requires 1 mandatory parameter, 'data,'
    with the additional optional parameters above. Examples:

    KAMA(self.data, period=self.params.period)
    KAMA(self.data, period=self.p.period, fast=self.p.fast, slow=self.p.slow)
    KAMA(self.data, period=10, fast=2, slow=30)
    KAMA(self.data)

    Formula: KAMA[0] = KAMA[-1] + SC(price - KAMA[-1])

    Where: SC = smoothing constant
    
    Additional information found at:
    https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/kaufmans-adaptive-moving-average-kama/
    https://www.fxcorporate.com/help/MS/NOTFIFO/i_Kama.html
    https://school.stockcharts.com/doku.php?id=technical_indicators:kaufman_s_adaptive_moving_average
    
    """

    lines = ('kama', )
    params = (('period', 10),   # efficiency ratio periods
              ('fast', 2),      # fast EMA periods
              ('slow', 30), )   # slow EMA periods

    plotinfo = dict(subplot=False)
    plotlines = dict(kama=dict(color='blue'))

    def __init__(self):
        direction = self.data - self.data(-self.params.period)

        # the following function is located within Backtrader's basicops.py module
        volatility = bt.ind.SumN(abs(self.data - self.data(-1)), period=self.params.period)

        # efficiency ratio
        er = abs(direction / volatility)

        fast = 2.0 / (self.params.fast + 1.0)
        slow = 2.0 / (self.params.slow + 1.0)

        # smoothing constant
        sc = pow((er * (fast - slow)) + slow, 2)

        # the following function is located within Backtrader's basicops.py module
        self.lines.kama = bt.ind.ExponentialSmoothingDynamic(self.data,
                                                    period=self.params.period,
                                                    alpha=sc)

class ZeroLagEMA(bt.Indicator):

    """
    Zero-Lag Exponential Moving Average - as the name suggests,
    works to reduce the lag associated with trend following
    indicators by attempting to remove lag from the data prior
    to the EMA calculation. This helps to limit the cumulative
    effect of data lag on the moving average.

    The default period is set to 20, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    ZeroLagEMA(self.data, period=self.params.period)
    ZeroLagEMA(self.data, period=self.p.period)
    ZeroLagEMA(self.data, period=20)
    ZeroLagEMA(self.data)

    Formula: EMA(clean data, period)

    Where:  lag = (period - 1) // 2
            clean data = 2 * data - data(lag days ago)

    Additional information found at:
    https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average
    https://user42.tuxfamily.org/chart/manual/Zero_002dLag-Exponential-Moving-Average.html
    https://www.quantifiedstrategies.com/zero-lag-exponential-moving-average/
    
    """

    lines = ('zero_lag_ema', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(zero_lag_ema=dict(color='blue'))

    def __init__(self):
        # component for reducing data lag
        lag = (self.params.period - 1) // 2
        clean_data = 2 * self.data - self.data(-lag)

        self.lines.zero_lag_ema = EMA(clean_data, period=self.params.period)

class TMA(bt.Indicator):

    """
    Triangular Moving Average - a second order simple moving average
    with a weighted component, the increments of which are assigned
    in a triangular pattern.

    The default period is set to 14, but can be overridden when
    calling the function.

    Requires 1 mandatory parameter, 'data,' with an additional
    optional parameter, 'period.' Examples:

    TMA(self.data, period=self.params.period)
    TMA(self.data, period=self.p.period)
    TMA(self.data, period=14)
    TMA(self.data)

    Formula: SMA(SMA(self.data, p2), p1)

    Where: p1 and p2 vary depending on the period

    Additional information found at:
    https://www.fxcorporate.com/help/MS/NOTFIFO/i_TMA.html
    https://fxcodebase.com/wiki/index.php/Triangular_Moving_Average_(TMA)
    
    """

    lines = ('tma', )
    params = (('period', 14), )

    plotinfo = dict(subplot=False)
    plotlines = dict(tma=dict(color='blue'))

    def __init__(self):
        p = self.params.period

        if p % 2:
            p1 = p2 = (p + 1) // 2 # p values for an odd number sample

        else:
            p1, p2 = (p // 2) + 1, p // 2 # p values for an even number sample

        self.lines.tma = SMA(SMA(self.data, period=p2), period=p1)