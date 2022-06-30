#!/usr/bin/env python
import os
import sys

import requests
import matplotlib
from datetime import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
import quantstats
import webbrowser

import enular 

ee = enular.Cerebro(optreturn = False)
data = enular.YahooData(dataname='TSLA', fromdate=datetime(2017, 1, 1), todate=datetime(2022, 1, 1))
ee.adddata(data)
ee.addstrategy(enular.strategies.CustomStrategy, indicator_a = bt.indicators.MovingAverageSimple, indicator_b = enular.indicators.CustomMASlow)
results = ee.run()
ee.plot()
