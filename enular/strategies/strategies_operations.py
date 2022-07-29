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

class VTOCrossover(enular.StrategyOperation):

    def trade_logic(self):
                  
        if self.indicator_a[0] > self.indicator_b[0] and self.indicator_a[-1] < self.indicator_b[-1]:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()

        elif self.indicator_a[0] < self.indicator_b[0] and self.indicator_a[-1] > self.indicator_b[-1]:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()

class BTOAnd(enular.StrategyOperation):

    def trade_logic(self):
                  
        #print(self.indicator_a[0])

        if self.indicator_a[0] >= 1.0 and self.indicator_b[0] >= 1.0:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()
            
        elif self.indicator_a[0] <= -1.0 and self.indicator_b[0] <= -1.0:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()

class BTOOr(enular.StrategyOperation):

    def trade_logic(self):
                  
        if self.indicator_a[0] >= 1 or self.indicator_b[0]>= 1:
            self.log(f'BUY CREATE {self.dataclose[0]:2f}')
            self.order = self.buy()
            
        elif self.indicator_a[0] <= -1 or self.indicator_b[0] <= -1:
            self.log(f'SELL CREATE {self.dataclose[0]:2f}')
            self.order = self.sell()
