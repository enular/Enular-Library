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
from backtrader.indicators import Average

import enular

class Dummy(enular.Indicator):    
    pass

class CustomBoolToBoolAnd(enular.Indicator):
    pass

class CustomScalarToBool(enular.Indicator):
    
    _mindatas = 2

    lines = ('crossover',)

    plotinfo = dict(plotymargin=0.05, plotyhlines=[-1.0, 1.0])

    def __init__(self):
        upcross = bt.indicator.CrossUp(self.data, self.data1)
        downcross = bt.indicator.CrossDown(self.data, self.data1)

        self.lines.crossover = upcross - downcross

    pass

class CustomMAFast(bt.indicators.MovingAverageSimple):    
    params = (('period',20),)

class CustomMASlow(bt.indicators.MovingAverageSimple):
    params = (('period',50),)

class CustomCrossOver(bt.indicators.CrossOver):

    params = (('pfast',20),('pslow',50),)

    def __init__(self):

        self.data0 = CustomMAFast(self.data, period = self.params.pfast)
        self.data1 = CustomMASlow(self.data, period = self.params.pslow)

        upcross = bt.indicators.CrossUp(self.data0, self.data1)
        downcross = bt.indicators.CrossDown(self.data0, self.data1)

        self.lines.crossover = upcross - downcross

class MovingAverageSimple(bt.indicators.MovingAverageSimple):
    pass

class CustomMLIndicator(enular.Indicator):    
    
    def init(self, model, data):
        pass