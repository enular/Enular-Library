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
import enularlib.indicators as indicators
import enularlib

#Scalar
#Formula:   AcdDecOsc = AwesomeOscillator - SMA(AwesomeOscillator, period)
#Scale:     Change in difference in average price
class AccelerationDecelerationOscillator(indicators.AccelerationDecelerationOscillator):
    pass

#Scalar
#Formula:   median price = (high + low) / 2
#           AO = SMA(median price, 5)- SMA(median price, 34)
#Scale:     Difference in average price
class AwesomeOscillator(indicators.AwesomeOscillator):
    pass

#Scalar
#Forumala:  aroonosc = aroonup - aroondown
#           up = 100 * (period - distance to highest high) / period
#           down = 100 * (period - distance to lowest low) / period
#Scale:     Period between peaks
class AroonOscillator(indicators.AroonOscillator):
    pass

#Scalar
#Formula:   TrueRange = max(high - low, abs(high - prev_close), abs(prev_close - low)
#           ATR = SmoothedMovingAverage(TrueRange, period)
#Scale:     Price range
class AverageTrueRange(indicators.AverageTrueRange):
    pass

#Scalar
#Scale:     Average price plus or minus standard deviations
#Note:      As 3 lines, mid, top, and bot
class BollingerBands(indicators.BollingerBands):
    pass

#Scalar
#Scale:     Percentage
class BollingerBandsPerc(indicators.BBPerc):
    pass

#Scalar    
#Scale:     Ratio
class CommodityChannelIndex(indicators.CommodityChannelIndex):
    pass

#Scalar
#Scale:     Price
class DoubleEMA(indicators.DoubleExponentialMovingAverage):
    pass

#Scalar:    Price
class TripleEMA(indicators.TripleExponentialMovingAverage):
    pass

#Scale:     Standard deviation
class StandardDeviation(indicators.StandardDeviation):
    pass

#Scalar:    Deviation
class MeanDeviation(indicators.MeanDeviation):
    pass

#Scalar:    Price movement
class DirectionalIndicator(indicators.DirectionalIndicator):
    pass

#Scalar:    Price movement up
class PlusDirectionalIndicator(indicators.PlusDirectionalIndicator):
    pass

#Scalar:    Price movement down
class MinusDirectionalIndicator(indicators.MinusDirectionalIndicator):
    pass

#Scalar:    Price movement average
class AverageDirectionalMovementIndex(indicators.AverageDirectionalMovementIndex):
    pass

#Scalar:
class AverageDirectionalMovementIndexRating(indicators.AverageDirectionalMovementIndexRating):
    pass

#Scalar:
class DirectionalMovementIndex(indicators.DirectionalMovementIndex):
    pass

#Scalar:
class DirectionalMovement(indicators.DirectionalMovement):
    pass

#Scalar:
class DicksonMovingAverage(indicators.DicksonMovingAverage):
    pass

#Scalar:
class DetrendedPriceOscillator(indicators.DetrendedPriceOscillator):
    pass

#Scalar:
class DV2(indicators.DV2):
    pass

#Scalar:
class ExponentialMovingAverage(indicators.ExponentialMovingAverage):
    pass

#Scalar
class Envelope(indicators.Envelope):
    pass

#Scalar:
class HADelta(indicators.HADelta):
    pass

#Scalar:
class HullMovingAverage(indicators.HullMovingAverage):
    pass

#Scalar:
class Ichimoku(indicators.Ichimoku):
    pass

#Scalar:
class AdaptiveMovingAverage(indicators.AdaptiveMovingAverage):
    pass

#Scalar:
class KnowSureThing(indicators.KnowSureThing):
    pass

#Scalar:
class LaguerreRSI(indicators.LaguerreRSI):
    pass

#Scalar:
class LaguerreFilter(indicators.LaguerreFilter):
    pass

#Scalar:
class MACD(indicators.MACD):
   pass

#Scalar:
class MACDHisto(indicators.MACDHisto):
    pass

#Scalar:
class Momentum(indicators.Momentum):
    pass

#Scalar:
class MomentumOscillator(indicators.MomentumOscillator):
    pass

#Scalar:
class RateOfChange(indicators.RateOfChange):
    pass

#Scalar:
class RateOfChange100(indicators.RateOfChange100):
    pass

#Scalar:
class OscillatorMixIn(indicators.OscillatorMixIn):
    pass

#Scalar:
class Oscillator(indicators.Oscillator):
    pass

#Scalar:
class PercentChange(indicators.PercentChange):
    pass

#Scalar:
class PercentRank(indicators.PercentRank):
    pass

#Scalar:
class PivotPoint(indicators.PivotPoint):
    pass

#Scalar:
class FibonacciPivotPoint(indicators.FibonacciPivotPoint):
    pass

#Scalar:
class DemarkPivotPoint(indicators.DemarkPivotPoint):
    pass

#Scalar:
class PrettyGoodOscillator(indicators.PrettyGoodOscillator):
    pass

#Scalar:
class PriceOscillator(indicators.PriceOscillator):
    pass

#Scalar:
class PercentagePriceOscillator(indicators.PercentagePriceOscillator):
    pass

#Scalar:
class ParabolicSAR(indicators.ParabolicSAR):
    pass

#Scalar:
class RelativeMomentumIndex(indicators.RelativeMomentumIndex):
    pass

#Scalar:
class RelativeStrengthIndex(indicators.RelativeStrengthIndex):
    pass

#Scalar:
class SmoothedMovingAverage(indicators.SmoothedMovingAverage):
    pass

#Scalar:
class StochasticFast(indicators.StochasticFast):
    pass

#Scalar:
class Stochastic(indicators.Stochastic):
    pass

#Scalar:
class StochasticFull(indicators.StochasticFull):
    pass

#Scalar:
class TRIXSignal(indicators.TRIXSignal):
    pass

#Scalar:
class TrueStrengthIndex(indicators.TrueStrengthIndex):
    pass

#Scalar
#Scale:     Percentage (or Ratio if not x100)
class UltimateOscillator(indicators.UltimateOscillator):
    pass

#Scalar:
class Vortex(indicators.Vortex):
    pass

#Scalar:
class WilliamsR(indicators.WilliamsR):
    pass

#Scalar:
class WilliamsAD(indicators.WilliamsAD):
    pass

#Scalar:
class WeightedMovingAverage(indicators.WeightedMovingAverage):
    pass

#Scalar:
class ZeroLagExponentialMovingAverage(indicators.ZeroLagExponentialMovingAverage):
    pass

#Scalar:
class ZeroLagIndicator(indicators.ZeroLagIndicator):
    pass

#Scalar
class SMAFast(indicators.SMA):    
    params = (('period',20),)

#Scalar
class SMASlow(indicators.SMA):
    params = (('period',50),)

#Scalar: diff = data - data1, upcross =  last_non_zero_diff < 0 and data0(0) > data1(0), downcross = last_non_zero_diff > 0 and data0(0) < data1(0), crossover = upcross - downcross
class CrossOver(indicators.CrossOver):

    params = (('pfast',20),('pslow',50),)

    lines = ('crossover',)

    def __init__(self):

        self.data0 = SMAFast(self.data, period = self.params.pfast)
        self.data1 = SMASlow(self.data, period = self.params.pslow)

        upcross = indicators.CrossUp(self.data0, self.data1)
        downcross = indicators.CrossDown(self.data0, self.data1)

        self.lines.crossover = upcross - downcross

#Boolean
#class MachineLearningClassify(enularlib.IndicatorOperation):    
#    def __init__(self):
#
#        pass

#Scalar
#class MachineLearningRegression(enularlib.IndicatorOperation):    
#
#    def __init__(self):
#        pass