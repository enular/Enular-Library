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

class CustomMAFast(bt.indicators.MovingAverageSimple):    
    params = (('period',20),)

class CustomMASlow(bt.indicators.MovingAverageSimple):
    params = (('period',52),)



class MovingAverageSimple(bt.indicators.MovingAverageSimple):

    pass

class CrossOver(bt.indicators.CrossOver):
    pass

#Custom indicators that inherit from the Indicator base class
class CustomIndicator(enular.Indicator):    
    
    def init(self, model, data):
        pass