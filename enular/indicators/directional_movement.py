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

from . import Indicator, And, If, MovAv, ATR



class UpMove(Indicator):

    """Up Move - part of the Directional Move System developed by
    J. Welles Wilder, Jr. to calculate directional indicators.

    The output value is positive if the price in the given data period is higher
    than that of the previous period.

    Formula:

        - up = data[0] - data[-1]

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    
    """

    lines = ('upmove', )

    def __init__(self):
        self.lines.upmove = self.data - self.data(-1)

        super(UpMove, self).__init__()


class DownMove(Indicator):

    """Down Move - part of the Directional Move System developed by
    J. Welles Wilder, Jr. to calculate directional indicators.

    The output value is positive if the price in the given data period is lower
    than that of the previous period.

    Formula:

        - down = data[-1] - data[0]

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    
    """

    lines = ('downmove', )

    def __init__(self):
        self.lines.downmove = self.data(-1) - self.data

        super(DownMove, self).__init__()


class _DirectionalIndicator(Indicator):

    """Serves as the root base class for all Directional Movement System related
    indicators, given that the calculations are initially common among all
    variations and further calculations are subsequently derived from these.

    Calculates the +DI and -DI values (using kwargs to know what to calculate)
    but does not assign them to lines, as subclasses are responsible for this.
    
    """

    params = (('period', 14), ('_movav', MovAv.Smoothed))

    plotlines = dict(plusDI=dict(_name='+DI', color='crimson'),
                     minusDI=dict(_name='-DI', color='navy'))

    def _plotlabel(self):
        plabels = [self.params.period, self.params._movav]
        return plabels

    def __init__(self, _plus=True, _minus=True):
        atr = ATR(self.data, period=self.params.period, _movav=self.params._movav)

        upmove = self.data.high - self.data.high(-1)
        downmove = self.data.low(-1) - self.data.low

        if _plus:
            plus = And(upmove > downmove, upmove > 0.0)
            plusDM = If(plus, upmove, 0.0)
            plusDMav = self.params._movav(plusDM, period=self.params.period)

            self.DIplus = 100.0 * plusDMav / atr

        if _minus:
            minus = And(downmove > upmove, downmove > 0.0)
            minusDM = If(minus, downmove, 0.0)
            minusDMav = self.params._movav(minusDM, period=self.params.period)

            self.DIminus = 100.0 * minusDMav / atr

        super(_DirectionalIndicator, self).__init__()


class DirectionalIndicator(_DirectionalIndicator):

    """Directional Indicator - this indicator assists in determining whether
    price is trending and attempts to measure the strength of that trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DirectionalIndicator(self.data, period=self.params.period)
        - DirectionalIndicator(self.data, period=self.p.period)
        - DirectionalIndicator(self.data, period=14)
        - DirectionalIndicator(self.data)

    This indicator shows +DI and -DI. For others in the set, use:

        - PlusDirectionalIndicator (PlusDI) to get +DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndex (ADX) to get ADX
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)
        - -DI = 100 * SMMA(-dm, period) / ATR(period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DirectionalIndicator(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = ('DI', )
    lines = ('plusDI', 'minusDI')

    def __init__(self):
        super(DirectionalIndicator, self).__init__()

        self.lines.plusDI = self.DIplus
        self.lines.minusDI = self.DIminus


class PlusDirectionalIndicator(_DirectionalIndicator):

    """Plus Directional Indicator - this indicator assists in determining
    whether price is trending and attempts to measure the strength of that
    trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - PlusDirectionalIndicator(self.data, period=self.params.period)
        - PlusDirectionalIndicator(self.data, period=self.p.period)
        - PlusDirectionalIndicator(self.data, period=14)
        - PlusDirectionalIndicator(self.data)

    This indicator only shows +DI. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndex (ADX) to get ADX
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - PlusDirectionalIndicator(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = (('PlusDI', '+DI'), )
    lines = ('plusDI', )

    plotinfo = dict(plotname='+DirectionalIndicator')
    plotlines = dict(plusDI=dict(_name='+DI', color='navy'))

    def __init__(self):
        super(PlusDirectionalIndicator, self).__init__(_minus=False)

        self.lines.plusDI = self.DIplus


class MinusDirectionalIndicator(_DirectionalIndicator):

    """Minus Directional Indicator - this indicator assists in determining
    whether price is trending and attempts to measure the strength of that
    trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - MinusDirectionalIndicator(self.data, period=self.params.period)
        - MinusDirectionalIndicator(self.data, period=self.p.period)
        - MinusDirectionalIndicator(self.data, period=14)
        - MinusDirectionalIndicator(self.data)

    This indicator only shows -DI. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - PlusDirectionalIndicator (PlusDI) to get +DI
        - AverageDirectionalIndex (ADX) to get ADX
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - -DI = 100 * SMMA(-dm, period) / ATR(period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - MinusDirectionalIndicator(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = (('MinusDI', '-DI'), )
    lines = ('minusDI', )

    plotinfo = dict(plotname='-DirectionalIndicator')
    plotlines = dict(plusDI=dict(_name='-DI', color='navy'))

    def __init__(self):
        super(MinusDirectionalIndicator, self).__init__(_plus=False)

        self.lines.minusDI = self.DIminus


class AverageDirectionalMovementIndex(_DirectionalIndicator):

    """Average Directional Movement Index - this indicator assists in
    determining whether price is trending and attempts to measure the
    strength of that trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - AverageDirectionalMovementIndex(self.data, period=self.params.period)
        - AverageDirectionalMovementIndex(self.data, period=self.p.period)
        - AverageDirectionalMovementIndex(self.data, period=14)
        - AverageDirectionalMovementIndex(self.data)

    This indicator only shows ADX. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - PlusDirectionalIndicator (PlusDI) to get +DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)
        - -DI = 100 * SMMA(-dm, period) / ATR(period)
        - dx = 100 * abs(+DI - -DI) / (+DI + -DI)
        - ADX = SMMA(dx, period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - AverageDirectionalMovementIndex(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = ('ADX', )
    lines = ('adx', )

    plotlines = dict(adx=dict(_name='ADX', color='forestgreen'))

    def __init__(self):
        super(AverageDirectionalMovementIndex, self).__init__()

        dx = abs(self.DIplus - self.DIminus) / (self.DIplus + self.DIminus)
        self.lines.adx = 100.0 * self.params._movav(dx, period=self.params.period)


class AverageDirectionalMovementIndexRating(AverageDirectionalMovementIndex):

    """Average Directional Movement Index Rating - this indicator assists
    in determining whether price is trending and attempts to measure the
    strength of that trend. It is the average of the current ADX and the
    ADX value with a lookback period.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but can be overridden when calling
    the function.

    Requires 1 mandatory parameter, 'data,' with an additional optional
    parameter, 'period.' Examples:

        - AverageDirectionalMovementIndexRating(self.data, period=self.params.period)
        - AverageDirectionalMovementIndexRating(self.data, period=self.p.period)
        - AverageDirectionalMovementIndexRating(self.data, period=14)
        - AverageDirectionalMovementIndexRating(self.data)

    This indicator shows ADX and ADXR. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - PlusDirectionalIndicator (PlusDI) to get +DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndex (ADX) to get ADX
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)
        - -DI = 100 * SMMA(-dm, period) / ATR(period)
        - dx = 100 * abs(+DI - -DI) / (+DI + -DI)
        - ADX = SMMA(dx, period)
        - ADXR = (ADX + ADX(-period)) / 2

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - AverageDirectionalMovementIndexRating(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = ('ADXR', )
    lines = ('adxr', )
    
    plotlines = dict(adxr=dict(_name='ADXR', color='darkorange'))

    def __init__(self):
        super(AverageDirectionalMovementIndexRating, self).__init__()

        self.lines.adxr = (self.lines.adx + self.lines.adx(-self.params.period)) / 2.0


class DirectionalMovementIndex(AverageDirectionalMovementIndex, DirectionalIndicator):
    
    """Directional Movement Index - this indicator assists in determining
    whether price is trending and attempts to measure the strength of that
    trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DirectionalMovementIndex(self.data, period=self.params.period)
        - DirectionalMovementIndex(self.data, period=self.p.period)
        - DirectionalMovementIndex(self.data, period=14)
        - DirectionalMovementIndex(self.data)

    This indicator shows ADX, +DI, and -DI. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - PlusDirectionalIndicator (PlusDI) to get +DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndex (ADX) to get ADX
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovement (DM) to get ADX, ADXR, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)
        - -DI = 100 * SMMA(-dm, period) / ATR(period)
        - dx = 100 * abs(+DI - -DI) / (+DI + -DI)
        - ADX = SMMA(dx, period)

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DirectionalMovementIndex(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """

    alias = ('DMI', )


class DirectionalMovement(AverageDirectionalMovementIndexRating, DirectionalIndicator):
    
    """Directional Movement - this indicator assists in determining whether
    price is trending and attempts to measure the strength of that trend.

    The moving average used is the Smoothed Moving Average (SMMA), along
    with the Average True Range (ATR).

    The default period is set to 14, but this can be overridden when calling the
    function.

    Requires one mandatory parameter, 'data', with an additional optional
    parameter, 'period'. Examples:

        - DirectionalMovement(self.data, period=self.params.period)
        - DirectionalMovement(self.data, period=self.p.period)
        - DirectionalMovement(self.data, period=14)
        - DirectionalMovement(self.data)

    This indicator shows ADX, ADXR, +DI, and -DI. For others in the set, use:

        - DirectionalIndicator (DI) to get +DI and -DI
        - PlusDirectionalIndicator (PlusDI) to get +DI
        - MinusDirectionalIndicator (MinusDI) to get -DI
        - AverageDirectionalIndex (ADX) to get ADX
        - AverageDirectionalIndexRating (ADXR) to get ADX and ADXR
        - DirectionalMovementIndex (DMI) to get ADX, +DI, and -DI

    Formula:

        - +dm = upmove if upmove > downmove and upmove > 0 else 0
        - -dm = downmove if downmove > upmove and downmove > 0 else 0
        - +DI = 100 * SMMA(+dm, period) / ATR(period)
        - -DI = 100 * SMMA(-dm, period) / ATR(period)
        - dx = 100 * abs(+DI - -DI) / (+DI + -DI)
        - ADX = SMMA(dx, period)
        - ADXR = (ADX + ADX(-period)) / 2

    Notes:

        - Although the standard moving average is the SMMA, this can be switched
          to any other. For example, use WMA by including _movav=WMA in the
          function.
        - DirectionalMovement(self.data, _movav=WMA)

    Additional information found at:
    https://en.wikipedia.org/wiki/Average_directional_movement_index
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi
    https://www.investopedia.com/terms/d/dmi.asp

    """
    
    alias = ('DM', )