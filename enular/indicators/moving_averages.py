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

from . import Indicator, basic_ops, ma_base

from . import (Indicator, MovAv, Average, AverageWeighted,
               ExponentialSmoothing, ExponentialSmoothingDynamic,
               SumN, MovingAverageBase)

from ..utils.py3 import MAXINT



class SimpleMovingAverage(Indicator):
    
    """Simple Moving Average - calculates the average price over 'n' periods.
    
    The default period is set to 50, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - SimpleMovingAverage(self.data, period=self.params.period)
        - SimpleMovingAverage(self.data, period=self.p.period)
        - SimpleMovingAverage(self.data, period=50)
        - SimpleMovingAverage(self.data)

    Formula:
    
        - sum(data, period) / (period)

    Additional information found at:
    https://www.investopedia.com/terms/s/sma.asp
    https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average

    """

    alias = ('SMA', 'MovingAverageSimple')
    lines = ('sma', )
    params = (('period', 50), )

    plotinfo = dict(subplot=False)
    plotlines = dict(sma=dict(color='navy'))

    def __init__(self):
        self.lines.sma = Average(self.data, period=self.params.period)

        super(SimpleMovingAverage, self).__init__()


class SMA(SimpleMovingAverage):

    """Alias for use within functions"""


class SmoothedMovingAverage(Indicator):

    """Smoothed Moving Average - similar to EMA, applies a weighting factor to
    each data point in the moving average sum, favouring the most recent. The
    weighting of all subsequent data points decreases exponentially, never
    reaching zero.

    The default period is set to 28, but can be overridden when calling the
    function. 14 and 28 are typically used for short-term trades, whereas 50,
    100 and 200 are typically used for identifying long-term trends.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - SmoothedMovingAverage(self.data, period=self.params.period)
        - SmoothedMovingAverage(self.data, period=self.p.period)
        - SmoothedMovingAverage(self.data, period=28)
        - SmoothedMovingAverage(self.data)
    
    Formula:
    
        - data[0] * (smoothing factor / (1 + period)) + SMMA[-1] * (1 - (smoothing factor / 1 + period))
    
    Additional information found at:
    https://www.tradingview.com/support/solutions/43000591343-smoothed-moving-average/
    https://www.quantifiedstrategies.com/smoothed-moving-average/
    
    """

    alias = ('SMMA', 'WilderMA', 'MovingAverageSmoothed',
             'MovingAverageWilder', 'ModifiedMovingAverage')
    lines = ('smma', )
    params = (('period', 28), )

    plotinfo = dict(subplot=False)
    plotlines = dict(smma=dict(color='navy'))

    def __init__(self):
        self.lines.smma = ExponentialSmoothing(self.data,
                                               period=self.params.period,
                                               alpha=1.0 / self.params.period)
                                               # alpha (smoothing factor)
        
        super(SmoothedMovingAverage, self).__init__()


class SMMA(SmoothedMovingAverage):

    """Alias for use within functions"""


class ExponentialMovingAverage(Indicator):
    
    """Exponential Moving Average - applies a weighting factor to each data
    point in the moving average sum, favouring the most recent. The weighting
    of all subsequent data points decreases exponentially, never reaching zero.

    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - ExponentialMovingAverage(self.data, period=self.params.period)
        - ExponentialMovingAverage(self.data, period=self.p.period)
        - ExponentialMovingAverage(self.data, period=20)
        - ExponentialMovingAverage(self.data)
    
    Formula:
    
        - data[0] * (smoothing factor / (1 + period)) + EMA[-1] * (1 - (smoothing factor / 1 + period))
    
    Additional information found at:
    https://www.investopedia.com/terms/e/ema.asp
    https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    
    """

    alias = ('EMA', 'MovingAverageExponential')
    lines = ('ema', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(ema=dict(color='navy'))

    def __init__(self):
        self.lines.ema = es = ExponentialSmoothing(self.data,
                                                   period=self.params.period,
                                                   alpha=2.0 / (1.0 + self.params.period))
                                                   # alpha (smoothing factor)

        # used in the zero lag indicator
        self.alpha, self.alpha1 = es.alpha, es.alpha1

        super(ExponentialMovingAverage, self).__init__()


class EMA(ExponentialMovingAverage):

    """Alias for use within functions"""


class DoubleExponentialMovingAverage(Indicator):

    """Double Exponential Moving Average - attempts to reduce the lag associated
    with with moving averages by applying additional weight on recent data
    points. This is not achieved by doubling the smoothing factor, rather, by
    subtracting a second order EMA from the doubled EMA.
    
    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DoubleExponentialMovingAverage(self.data, period=self.params.period)
        - DoubleExponentialMovingAverage(self.data, period=self.p.period)
        - DoubleExponentialMovingAverage(self.data, period=20)
        - DoubleExponentialMovingAverage(self.data)

    Formula:
    
        - 2*EMA - EMA(EMA)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DoubleExponentialMovingAverage(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/d/double-exponential-moving-average.asp
    https://en.wikipedia.org/wiki/Double_exponential_moving_average
    
    """

    alias = ('DEMA', 'MovingAverageDoubleExponential')
    lines = ('double_ema', )
    params = (('period', 20), ('_movav', MovAv.Exponential))

    plotinfo = dict(subplot=False)
    plotlines = dict(double_ema=dict(color='navy'))

    def __init__(self):
        ema1 = self.params._movav(self.data, period=self.params.period)
        ema2 = self.params._movav(ema1, period=self.params.period)

        self.lines.double_ema = 2.0 * ema1 - ema2

        super(DoubleExponentialMovingAverage, self).__init__()


class DoubleEMA(DoubleExponentialMovingAverage):

    """Alias for use within functions"""


class TripleExponentialMovingAverage(Indicator):

    """Triple Exponential Moving Average - attempts to reduce the lag associated
    with with moving averages by applying additional weight on recent data
    points. This is not achieved by tripling the smoothing factor, rather, by
    subtracting a second order EMA 3 times from the tripled EMA before adding a
    3rd order EMA.

    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - TripleExponentialMovingAverage(self.data, period=self.params.period)
        - TripleExponentialMovingAverage(self.data, period=self.p.period)
        - TripleExponentialMovingAverage(self.data, period=20)
        - TripleExponentialMovingAverage(self.data)

    Formula:
    
        - 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - TripleExponentialMovingAverage(self.data, _movav=WMA)

    Additional information found at:
    https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
    https://en.wikipedia.org/wiki/Triple_exponential_moving_average
    
    """

    alias = ('TEMA', 'MovingAverageTripleExponential')
    lines = ('triple_ema', )
    params = (('period', 20), ('_movav', MovAv.Exponential))

    plotinfo = dict(subplot=False)
    plotlines = dict(triple_ema=dict(color='navy'))

    def __init__(self):
        ema1 = self.params._movav(self.data, period=self.params.period)
        ema2 = self.params._movav(ema1, period=self.params.period)
        ema3 = self.params._movav(ema2, period=self.params.period)

        self.lines.triple_ema = 3.0 * ema1 - 3.0 * ema2 + ema3

        super(TripleExponentialMovingAverage, self).__init__()


class TripleEMA(TripleExponentialMovingAverage):

    """Alias for use within functions"""


class WeightedMovingAverage(Indicator):

    """Weighted Moving Average - applies a fixed weighting to the moving
    average, greatest at the most recent data point, decreasing
    arithmetically as the data points progress.

    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - WeightedMovingAverage(self.data, period=self.params.period)
        - WeightedMovingAverage(self.data, period=self.p.period)
        - WeightedMovingAverage(self.data, period=20)
        - WeightedMovingAverage(self.data)

    Formula:
    
        - weighting coefficient * sum(weight[i] * data[period - i] for i in range(period))

    Additional information found at:
    https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average
    
    """

    alias = ('WMA', 'MovingAverageWeighted')
    lines = ('wma', )
    params = (('period', 20), )

    plotinfo = dict(subplot=False)
    plotlines = dict(wma=dict(color='navy'))

    def __init__(self):
        # calculation for the weighting coefficient
        coef = 2.0 / (self.params.period * (self.params.period + 1.0))

        # weights for the look-back period
        weights = tuple(float(x) for x in range(1, self.params.period + 1))

        self.lines.wma = AverageWeighted(self.data,
                                                period=self.params.period,
                                                coef=coef,
                                                weights=weights)
        
        super(WeightedMovingAverage, self).__init__()


class WMA(WeightedMovingAverage):

    """Alias for use within functions"""


class HullMovingAverage(Indicator):

    """Hull Moving Average - derived from the weighted moving average with the
    objective of further reducing lag and improving smoothness.
    
    The default period is set to 16, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - HullMovingAverage(self.data, period=self.params.period)
        - HullMovingAverage(self.data, period=self.p.period)
        - HullMovingAverage(self.data, period=16)
        - HullMovingAverage(self.data)

    Formula:
    
        - WMA(2 * WMA(period // 2) - WMA(period), sqrt(period))

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use SMMA by including _movav=SMMA in the
          function.
        - HullMovingAverage(self.data, _movav=SMMA)

    Additional information found at:
    https://alanhull.com/hull-moving-average
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/hull-moving-average
    https://school.stockcharts.com/doku.php?id=technical_indicators:hull_moving_average
    
    """

    alias = ('HMA', 'HullMA')
    lines = ('hma', )
    params = (('period', 16), ('_movav', MovAv.Exponential))

    plotinfo = dict(subplot=False)
    plotlines = dict(hma=dict(color='navy'))

    def __init__(self):
        # first and second WMA values
        wma = self.params._movav(self.data, period=self.params.period)
        wma2 = 2.0 * self.params._movav(self.data, period=self.params.period // 2)

        sqrtperiod = pow(self.params.period, 0.5)

        self.lines.hma = self.params._movav(wma2 - wma, period=int(sqrtperiod))

        super(HullMovingAverage, self).__init__()


class HMA(HullMovingAverage):

    """Alias for use within functions"""


class DicksonMovingAverage(Indicator):

    """Dickson Moving Average - attempts to replicate the accuracy of a
    technique known as the Jurik Moving Average by combining the Zero Lag
    Indicator with the Hull Moving Average.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 20
        - gainlimit = 50
        - hull_period = 7

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DicksonMovingAverage(self.data, period=self.params.period)
        - DicksonMovingAverage(self.data, period=self.p.period, gainlimit=self.p.gainlimit, hull_period=self.p.hull_period)
        - DicksonMovingAverage(self.data, period=20, gainlimit=50, hull_period=7)
        - DicksonMovingAverage(self.data)

    Formula:
    
        - (ZeroLagIndicator(period, gainlimit) + HMA(hull_period)) / 2

    Notes:

        - Although the standard moving average is the HMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DicksonMovingAverage(self.data, _hma=WMA)

    Additional information found at:
    https://www.reddit.com/r/algotrading/comments/4xj3vh/dickson_moving_average
    
    """

    alias = ('DMA', 'DicksonMA')
    lines = ('dma', )
    params = (('period', 20),
              ('gainlimit', 50),
              ('hull_period', 7),
              ('_movav', MovAv.Exponential),
              ('_hma', MovAv.HMA))

    plotinfo = dict(subplot=False)
    plotlines = dict(dma=dict(color='navy'))

    def __init__(self):
        # error correcting component
        ec = ZeroLagIndicator(period=self.params.period,
                              gainlimit=self.params.gainlimit,
                              _movav=self.params._movav)

        # Hull component with reduced look-back period
        hull = self.params._hma(period=self.params.hull_period)

        self.lines.dma = (ec + hull) / 2.0

        super(DicksonMovingAverage, self).__init__()


class DMA(DicksonMovingAverage):

    """Alias for use within functions"""


class AdaptiveMovingAverage(MovingAverageBase):

    """Kaufman's Adaptive Moving Average - uses a fast and slow exponential
    smoothing component to filter out market noise whilst accounting for price
    and volatility.

    The speed of the indicator quickly adapts to new trends and is best utilised
    in a trending environment, as opposed to stagnant markets.

    This indicator requires three positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 10
        - fast = 2
        - slow = 30

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - AdaptiveMovingAverage(self.data, period=self.params.period)
        - AdaptiveMovingAverage(self.data, period=self.p.period, fast=self.p.fast, slow=self.p.slow)
        - AdaptiveMovingAverage(self.data, period=10, fast=2, slow=30)
        - AdaptiveMovingAverage(self.data)

    Formula:
    
        - KAMA[0] = KAMA[-1] + SC(price - KAMA[-1])

    Where:
    
        - SC = smoothing constant
    
    Additional information found at:
    https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/kaufmans-adaptive-moving-average-kama/
    https://www.fxcorporate.com/help/MS/NOTFIFO/i_Kama.html
    https://school.stockcharts.com/doku.php?id=technical_indicators:kaufman_s_adaptive_moving_average
    
    """

    alias = ('KAMA', 'MovingAverageAdaptive')
    lines = ('kama', )
    params = (('period', 10),   # efficiency ratio periods
              ('fast', 2),  # fast EMA periods
              ('slow', 30)) # slow EMA periods

    plotinfo = dict(subplot=False)
    plotlines = dict(kama=dict(color='blue'))

    def __init__(self):
        direction = self.data - self.data(-self.params.period)

        volatility = SumN(abs(self.data - self.data(-1)), period=self.params.period)

        # efficiency ratio
        er = abs(direction / volatility)

        fast = 2.0 / (self.params.fast + 1.0)
        slow = 2.0 / (self.params.slow + 1.0)

        # smoothing constant
        sc = pow((er * (fast - slow)) + slow, 2)

        self.lines.kama = ExponentialSmoothingDynamic(self.data,
                                                      period=self.params.period,
                                                      alpha=sc)
        
        super(AdaptiveMovingAverage, self).__init__()


class KAMA(AdaptiveMovingAverage):

    """Alias for use within functions"""


class ZeroLagExponentialMovingAverage(MovingAverageBase):

    """Zero-Lag Exponential Moving Average - as the name suggests, works to
    reduce the lag associated with trend following indicators by attempting to
    remove lag from the data prior to the EMA calculation. This helps to limit
    the cumulative effect of data lag on the moving average.

    The default period is set to 20, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - ZeroLagExponentialMovingAverage(self.data, period=self.params.period)
        - ZeroLagExponentialMovingAverage(self.data, period=self.p.period)
        - ZeroLagExponentialMovingAverage(self.data, period=20)
        - ZeroLagExponentialMovingAverage(self.data)

    Formula:
    
        - EMA(clean data, period)

    Where:
    
        - lag = (period - 1) // 2
        - clean data = 2 * data - data(lag days ago)

    Notes:

        - Although the standard moving average is the EMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - ZeroLagExponentialMovingAverage(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average
    https://user42.tuxfamily.org/chart/manual/Zero_002dLag-Exponential-Moving-Average.html
    https://www.quantifiedstrategies.com/zero-lag-exponential-moving-average/
    
    """

    alias = ('ZLEMA', 'ZeroLagEma')
    lines = ('zero_lag_ema', )
    params = (('period', 20), ('_movav', MovAv.Exponential))

    plotinfo = dict(subplot=False)
    plotlines = dict(zero_lag_ema=dict(color='navy'))

    def __init__(self):
        # component for reducing data lag
        lag = (self.params.period - 1) // 2
        clean_data = 2 * self.data - self.data(-lag)

        self.lines.zero_lag_ema = self.params._movav(clean_data, period=self.params.period)

        super(ZeroLagExponentialMovingAverage, self).__init__()


class TriangularMovingAverage(Indicator):

    """Triangular Moving Average - a second order simple moving average with a
    weighted component, the increments of which are assigned in a triangular
    pattern.

    The default period is set to 14, but can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - TriangularMovingAverage(self.data, period=self.params.period)
        - TriangularMovingAverage(self.data, period=self.p.period)
        - TriangularMovingAverage(self.data, period=14)
        - TriangularMovingAverage(self.data)

    Formula:
    
        - SMA(SMA(self.data, p2), p1)

    Where:
    
        - p1 and p2 vary depending on the period

    Notes:

        - Although the standard moving average is the SMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - TMA(self.data, _movav=WMA)

    Additional information found at:
    https://www.fxcorporate.com/help/MS/NOTFIFO/i_TMA.html
    https://fxcodebase.com/wiki/index.php/Triangular_Moving_Average_(TMA)
    
    """

    alias = ('TMA', 'MovingAverageTriangular')
    lines = ('tma', )
    params = (('period', 14), ('_movav', MovAv.Simple))

    plotinfo = dict(subplot=False)
    plotlines = dict(tma=dict(color='navy'))

    def __init__(self):
        p = self.params.period

        if p % 2:
            p1 = p2 = (p + 1) // 2 # p values for an odd number sample

        else:
            p1, p2 = (p // 2) + 1, p // 2 # p values for an even number sample

        self.lines.tma = self.params._movav(self.params._movav(self.data, period=p2), period=p1)

        super(TriangularMovingAverage, self).__init__()


class TMA(TriangularMovingAverage):

    """Alias for use within functions"""


class ZeroLagIndicator(MovingAverageBase):

    """Zero Lag Indicator - as the name suggests, works to reduce the lag
    associated with trend following indicators by attempting to minimise the
    error component.

    This indicator requires two positional arguments that can be overridden
    when calling the function. The default values are:

        - period = 20
        - gainlimit = 50

    Requires one mandatory parameter, 'data', with the additional optional
    parameters above. Examples:

        - ZeroLagIndicator(self.data, period=self.params.period)
        - ZeroLagIndicator(self.data, period=self.p.period, gainlimit=self.p.gainlimit)
        - ZeroLagIndicator(self.data, period=20, gainlimit=50)
        - ZeroLagIndicator(self.data)

    Formula:
    
        - EC[0] = alpha * (EMA + bestgain(closing price - EC[-1]) + (1 - alpha) * EC[-1])
        - Error = price - EC
    
    Additional information found at:
    https://www.mesasoftware.com/papers/ZeroLag.pdf

    """

    alias = ('ZLIndicator', 'ZLInd', 'EC', 'ErrorCorrecting')
    lines = ('ec', )
    params = (('period', 20),
              ('gainlimit', 50),
              ('_movav', MovAv.Exponential))

    plotlines = dict(ec=dict(color='navy'))

    def __init__(self):
        self.ema = self.params._movav(period=self.params.period)
        self.limits = [-self.params.gainlimit, self.params.gainlimit + 1]

        super(ZeroLagIndicator, self).__init__()

    def next(self):
        leasterror = MAXINT  # 1000000 in original code
        bestec = ema = self.ema[0]  # seed value 1st time for ec
        price = self.data[0]
        ec1 = self.lines.ec[-1]
        alpha, alpha1 = self.ema.alpha, self.ema.alpha1

        for value1 in range(*self.limits):
            gain = value1 / 10
            ec = alpha * (ema + gain * (price - ec1)) + alpha1 * ec1
            error = abs(price - ec)
            if error < leasterror:
                leasterror = error
                bestec = ec

        self.lines.ec[0] = bestec