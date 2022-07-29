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
import sklearn

import enular

class VTOCrossover(enular.Strategy):

    def trade_logic(self):
                  
        if self.indicator_a[0] > self.indicator_b[0] and self.indicator_a[-1] < self.indicator_b[-1]:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()

        elif self.indicator_a[0] < self.indicator_b[0] and self.indicator_a[-1] > self.indicator_b[-1]:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()

class BTOAnd(enular.Strategy):

    def trade_logic(self):
                  
        if self.indicator_a > 0 and self.indicator_b > 0:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()
            
        elif self.indicator_a < 0 and self.indicator_b < 0:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()

class BTOOr(enular.Strategy):

    def trade_logic(self):
                  
        if self.indicator_a > 0 or self.indicator_b > 0:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()
            
        elif self.indicator_a < 0 or self.indicator_b < 0:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()
