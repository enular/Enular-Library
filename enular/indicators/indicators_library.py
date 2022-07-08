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

#Scalar
#Formula:   AcdDecOsc = AwesomeOscillator - SMA(AwesomeOscillator, period)
#Scale:     Change in difference in average price
class AccelerationDecelerationOscillator(bt.indicators.AccelerationDecelerationOscillator):
    pass

#Scalar
#Formula:   median price = (high + low) / 2
#           AO = SMA(median price, 5)- SMA(median price, 34)
#Scale:     Difference in average price
class AwesomeOscillator(bt.indicators.AwesomeOscillator):
    pass

#Scalar
#Forumala:  aroonosc = aroonup - aroondown
#           up = 100 * (period - distance to highest high) / period
#           down = 100 * (period - distance to lowest low) / period
#Scale:     Period between peaks
class AroonOscillator(bt.indicators.AroonOscillator):
    pass

#Scalar
#Formula:   TrueRange = max(high - low, abs(high - prev_close), abs(prev_close - low)
#           ATR = SmoothedMovingAverage(TrueRange, period)
#Scale:     Price range
class AverageTrueRange(bt.indicators.AverageTrueRange):
    pass

#Scalar
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
class PlusDirectionalIndicator(bt.indicators.PlusDirectionalIndicator):
    pass

#Scalar:
class MinusDirectionalIndicator(bt.indicators.MinusDirectionalIndicator):
    pass

#Scalar:
class AverageDirectionalMovementIndex(bt.indicators.AverageDirectionalMovementIndex):
    pass

#Scalar:
class AverageDirectionalMovementIndexRating(bt.indicators.AverageDirectionalMovementIndexRating):
    pass

#Scalar:
class DirectionalMovementIndex(bt.indicators.DirectionalMovementIndex):
    pass

#Scalar:
class DirectionalMovement(bt.indicators.DirectionalMovement):
    pass

#Scalar:
class DicksonMovingAverage(bt.indicators.DicksonMovingAverage):
    pass

#Scalar:
class DetrendedPriceOscillator(bt.indicators.DetrendedPriceOscillator):
    pass

#Scalar:
class DV2(bt.indicators.DV2):
    pass

#Scalar:
class ExponentialMovingAverage(bt.indicators.ExponentialMovingAverage):
    pass

#Scalar:
class Envelope(bt.indicators.Envelope):
    pass

#Scalar:
class haDelta(bt.indicators.haDelta):
    pass

#Scalar:
class HeikinAshi(bt.indicators.HeikinAshi):
    pass

#Scalar:
class HullMovingAverage(bt.indicators.HullMovingAverage):
    pass

#Scalar:
class HurstExponent(bt.indicators.HurstExponent):
    pass

#Scalar:
class Ichimoku(bt.indicators.Ichimoku):
    pass

#Scalar:
class AdaptiveMovingAverage(bt.indicators.AdaptiveMovingAverage):
    pass

#Scalar:
class KnowSureThing(bt.indicators.KnowSureThing):
    pass

#Scalar:
class LaguerreRSI(bt.indicators.LaguerreRSI):
    pass

#Scalar:
class LaguerreFilter(bt.indicators.LaguerreFilter):
    pass

#Scalar:
class MACD(bt.indicators.MACD):
    pass

#Scalar:
class MACDHisto(bt.indicators.MACDHisto):
    pass

#Scalar:
class Momentum(bt.indicators.Momentum):
    pass

#Scalar:
class MomentumOscillator(bt.indicators.MomentumOscillator):
    pass

#Scalar:
class RateOfChange(bt.indicators.RateOfChange):
    pass

#Scalar:
class RateOfChange100(bt.indicators.RateOfChange100):
    pass

#Scalar:
class OLS_Slope_InterceptN(bt.indicators.OLS_Slope_InterceptN):
    pass

#Scalar:
class OLS_TransformationN(bt.indicators.OLS_TransformationN):
    pass

#Scalar:
class OLS_BetaN(bt.indicators.OLS_BetaN):
    pass

#Scalar:
class CointN(bt.indicators.CointN):
    pass

#Scalar:
class OscillatorMixIn(bt.indicators.OscillatorMixIn):
    pass

#Scalar:
class Oscillator(bt.indicators.Oscillator):
    pass

#Scalar:
class PercentChange(bt.indicators.PercentChange):
    pass

#Scalar:
class PercentRank(bt.indicators.PercentRank):
    pass

#Scalar:
class PivotPoint(bt.indicators.PivotPoint):
    pass

#Scalar:
class FibonacciPivotPoint(bt.indicators.FibonacciPivotPoint):
    pass

#Scalar:
class DemarkPivotPoint(bt.indicators.DemarkPivotPoint):
    pass

#Scalar:
class PrettyGoodOscillator(bt.indicators.PrettyGoodOscillator):
    pass

#Scalar:
class PriceOscillator(bt.indicators.PriceOscillator):
    pass

#Scalar:
class PercentagePriceOscillator(bt.indicators.PercentagePriceOscillator):
    pass

#Scalar:
class ParabolicSAR(bt.indicators.ParabolicSAR):
    pass

#Scalar:
class RelativeMomentumIndex(bt.indicators.RelativeMomentumIndex):
    pass

#Scalar:
class RelativeStrengthIndex(bt.indicators.RelativeStrengthIndex):
    pass

#Scalar:
class SmoothedMovingAverage(bt.indicators.SmoothedMovingAverage):
    pass

#Scalar:
class StochasticFast(bt.indicators.StochasticFast):
    pass

#Scalar:
class Stochastic(bt.indicators.Stochastic):
    pass

#Scalar:
class StochasticFull(bt.indicators.StochasticFull):
    pass

#Scalar:
class Trix(bt.indicators.Trix):
    pass

#Scalar:
class TrixSignal(bt.indicators.TrixSignal):
    pass

#Scalar:
class TrueStrengthIndicator(bt.indicators.TrueStrengthIndicator):
    pass

#Scalar:
class UltimateOscillator(bt.indicators.UltimateOscillator):
    pass

#Scalar:
class Vortex(bt.indicators.Vortex):
    pass

#Scalar:
class WilliamsR(bt.indicators.WilliamsR):
    pass

#Scalar:
class WilliamsAD(bt.indicators.WilliamsAD):
    pass

#Scalar:
class WeightedMovingAverage(bt.indicators.WeightedMovingAverage):
    pass

#Scalar:
class ZeroLagExponentialMovingAverage(bt.indicators.ZeroLagExponentialMovingAverage):
    pass

#Scalar:
class ZeroLagIndicator(bt.indicators.ZeroLagIndicator):
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