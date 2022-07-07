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
