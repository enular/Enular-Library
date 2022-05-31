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

from enular.enular_base import *

class MovingAverageSimple(bt.indicators.MovingAverageSimple):
    pass

class CrossOver(bt.indicators.CrossOver):
    pass

#Custom indicators that inherit from the Indicator base class
class CustomIndicator(Indicator):    
    
    def init(self, model, data):
        pass