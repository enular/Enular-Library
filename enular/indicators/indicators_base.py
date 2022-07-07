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

#Boolean
class MovingAverageFast(bt.indicators.MovingAverageSimple):    
    params = (('period',20),)

#Boolean
class MovingAverageSlow(bt.indicators.MovingAverageSimple):
    params = (('period',50),)

#Scalar
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