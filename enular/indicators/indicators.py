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

#Main

class Dummy(enular.Indicator):    
    pass

class CustomBoolToBoolAnd(enular.Indicator):
    
    params = (
        ('indicator_a',Dummy),
        ('indicator_b',Dummy),
    )

    lines = ('cbtba',)

    def __init__(self):

        self.data0 = self.params.indicator_a(self.data)
        self.data1 = self.params.indicator_b(self.data)

        and_operation = (self.data0 + self.data1)/2

        self.lines.cbtba = and_operation
        
class CustomScalarToBool(enular.Indicator):
    
    params = (
        ('indicator_a',Dummy),
        ('indicator_b',Dummy),
    )

    lines = ('cstb',)

    def __init__(self):

        self.data0 = self.params.indicator_a(self.data)
        self.data1 = self.params.indicator_b(self.data)

        upcross = bt.indicators.CrossUp(self.data0, self.data1)
        downcross = bt.indicators.CrossDown(self.data0, self.data1)

        self.lines.cstb = upcross - downcross

class CustomScalarToScalar(enular.Indicator):
    
    params = (
        ('indicator_a',Dummy),
        ('indicator_b',Dummy),
    )

    lines = ('csts',)

    def __init__(self):

        self.data0 = self.params.indicator_a(self.data)
        self.data1 = self.params.indicator_b(self.data)

        upcross = self.data0 + self.data1

        self.lines.csts = upcross - downcross

#Tests

class CustomMAFast(bt.indicators.MovingAverageSimple):    
    params = (('period',20),)

class CustomMASlow(bt.indicators.MovingAverageSimple):
    params = (('period',50),)

class CustomCrossOver(bt.indicators.CrossOver):

    params = (('pfast',20),('pslow',50),)

    lines = ('crossover',)

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