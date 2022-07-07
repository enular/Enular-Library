#!/usr/bin/env python
import os
import sys
import matplotlib
import yfinance
import numpy
import scipy
import sklearn
import pandas
import backtrader as bt

import enular

#Scalar: AcdDecOsc = AwesomeOscillator - SMA(AwesomeOscillator, period)
class AccelerationDecelerationOscillator(bt.indicators.AccelerationDecelerationOscillator):
    pass

#Scalar: median price = (high + low) / 2, AO = SMA(median price, 5)- SMA(median price, 34)
class AwesomeOscillator(bt.indicators.AwesomeOscillator):
    pass

#Scalar: aroonosc = aroonup - aroondown, up = 100 * (period - distance to highest high) / period, down = 100 * (period - distance to lowest low) / period
class AroonOscillator(bt.indicators.AroonOscillator):
    pass

#Scalar:
class AverageTrueRange(bt.indicators.AverageTrueRange):
    pass

#Scalar:
class BollingerBands(bt.indicators.BollingerBands):
    pass

#Scalar:
class BollingerBandsPct(bt.indicators.BollingerBandsPct):
    pass

#Scalar:
class CommodityChannelIndex(bt.indicators.CommodityChannelIndex):
    pass

#Scalar:
class DoubleExponentialMovingAverage(bt.indicators.DoubleExponentialMovingAverage):
    pass

#Scalar:
class TripleExponentialMovingAverage(bt.indicators.TripleExponentialMovingAverage):
    pass

#Scalar:
class StandardDeviation(bt.indicators.StandardDeviation):
    pass

#Scalar:
class MeanDeviation(bt.indicators.MeanDeviation):
    pass

#Scalar:
class DirectionalIndicator(bt.indicators.DirectionalIndicator):
    pass

#Scalar:
class DirectionalIndicator(bt.indicators.DirectionalIndicator):
    pass

#Scalar:
class DirectionalIndicator(bt.indicators.DirectionalIndicator):
    pass

#Scalar
class MovingAverageFast(bt.indicators.MovingAverageSimple):    
    params = (('period',20),)

#Scalar
class MovingAverageSlow(bt.indicators.MovingAverageSimple):
    params = (('period',50),)

#Scalar: diff = data - data1, upcross =  last_non_zero_diff < 0 and data0(0) > data1(0), downcross = last_non_zero_diff > 0 and data0(0) < data1(0), crossover = upcross - downcross
class CrossOver(bt.indicators.CrossOver):

    params = (('pfast',20),('pslow',50),)

    lines = ('crossover',)

    def __init__(self):

        self.data0 = MovingAverageFast(self.data, period = self.params.pfast)
        self.data1 = MovingAverageSlow(self.data, period = self.params.pslow)

        upcross = bt.indicators.CrossUp(self.data0, self.data1)
        downcross = bt.indicators.CrossDown(self.data0, self.data1)

        self.lines.crossover = upcross - downcross

#Boolean
class MachineLearningClassify(enular.Indicator):    

    def __init__(self):
        pass

#Scalar
class MachineLearningRegression(enular.Indicator):    

    def __init__(self):
        pass