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

class VTVCustom(enular.Indicator):

    lines = ('vtvcustom',)

    def trade_logic(self):

        operation = self.data0 + self.data1
        self.lines.vtvcustom = operation

class VTBCrossover(enular.Indicator):

    lines = ('vtbcrossover',)

    def trade_logic(self):

        upcross = bt.indicators.CrossUp(self.data0, self.data1)
        downcross = bt.indicators.CrossDown(self.data0, self.data1)
        operation = upcross - downcross
        self.lines.vtb = operation

class BTBAnd(enular.Indicator):

    lines = ('btband',)

    def trade_logic(self):

        operation = self.data0 * self.data1
        self.lines.btband = operation

class BTBOr(enular.Indicator):

    lines = ('btbor',)

    def trade_logic(self):

        operation = self.data0 + self.data1
        self.lines.btband = operation