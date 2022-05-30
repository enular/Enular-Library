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

class CustomIndicator(Indicator):
    
    pass