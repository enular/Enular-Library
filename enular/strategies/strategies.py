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

class CustomStrategy(enular.Strategy):
    
    params = (
        ('indicator_a',enular.indicators.Dummy),
        ('indicator_b',enular.indicators.Dummy),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        
        # Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate moving averages

        self.indicator_a = self.params.indicator_a(self.datas[0])
        self.indicator_b = self.params.indicator_b(self.datas[0])

        #self.indicator_a = enular.indicators.MovingAverageSimple(self.datas[0],period=20)
        #self.indicator_b = enular.indicators.MovingAverageSimple(self.datas[0],period=52)

        print(self.indicator_a)

    def next(self):
	# Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades
                
            if self.indicator_a[0] > self.indicator_b[0] and self.indicator_a[-1] < self.indicator_b[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
             
            elif self.indicator_a[0] < self.indicator_b[0] and self.indicator_a[-1] > self.indicator_b[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()

class MAcrossover(enular.Strategy): 
    # Moving average parameters
    params = (('pfast',20),('pslow',52),)

    def __init__(self, *args):
        self.dataclose = self.datas[0].close
        
        # Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate moving averages
        try:
            self.slow_sma = enular.indicators.MovingAverageSimple(self.datas[0], 
                            period=args[1])
            self.fast_sma = enular.indicators.MovingAverageSimple(self.datas[0], 
                            period=args[0])
        except:
            self.slow_sma = enular.indicators.MovingAverageSimple(self.datas[0], 
                            period=self.params.pslow)
            self.fast_sma = enular.indicators.MovingAverageSimple(self.datas[0], 
                            period=self.params.pfast)

        print(self.fast_sma)

        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)
    
    def next(self):
	# Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades
                
            #If the 20 SMA is above the 50 SMA
            #if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
            if self.crossover > 0: # Fast ma crosses above slow ma
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            #Otherwise if the 20 SMA is below the 50 SMA   
            #elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
            elif self.crossover < 0: # Fast ma crosses below slow ma
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()

class AverageTrueRange(enular.Strategy):

	def log(self, txt, dt=None):
		dt = dt or self.datas[0].datetime.date(0)
		print(f'{dt.isoformat()} {txt}') #Print date and close
		
	def __init__(self):
		self.dataclose = self.datas[0].close
		self.datahigh = self.datas[0].high
		self.datalow = self.datas[0].low
		
	def next(self):
		range_total = 0
		for i in range(-13, 1):
			true_range = self.datahigh[i] - self.datalow[i]
			range_total += true_range
		ATR = range_total / 14

		self.log(f'Close: {self.dataclose[0]:.2f}, ATR: {ATR:.4f}')

class MachineLearningClassify(enular.Strategy):
    pass

class MachineLearningRegression(enular.Strategy):
    pass

class MachineLearningReinforcement(enular.Strategy):
    pass