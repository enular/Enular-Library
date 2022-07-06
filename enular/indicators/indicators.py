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

#CORE

class ScalToScal(enular.Indicator):

    lines = ('sts',)

    def trade_logic(self):

        operation = self.data0 + self.data1
        self.lines.sts = operation



class ScalToBool(enular.Indicator):

    lines = ('stb',)

    def trade_logic(self):

        upcross = bt.indicators.CrossUp(self.data0, self.data1)
        downcross = bt.indicators.CrossDown(self.data0, self.data1)
        operation = upcross - downcross
        self.lines.stb = operation

class BoolToBool(enular.Indicator):

    lines = ('btb',)

    def trade_logic(self):

        operation = (self.data0 + self.data1)/2
        self.lines.btb = operation

#TEST

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