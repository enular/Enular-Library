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

#data = bt.feeds.PandasData(dataname=yf.download('TSLA','2017-01-01','2019-01-01'))
data = enular.YahooData(dataname='TSLA', fromdate=datetime(2017, 1, 1), todate=datetime(2022, 1, 1))

ee.adddata(data)

ee.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__' and sys.argv[1] == 'test':
    
    ee.addstrategy(enular.strategies.CustomStrategy, indicator_a = bt.indicators.MovingAverageSimple, indicator_b = enular.indicators.CustomMASlow)
    
    ee.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

    start_portfolio_value = ee.broker.getvalue()

    results = ee.run()

    end_portfolio_value = ee.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    #ee.quantstats(results)
    ee.plot()

if __name__ == '__main__' and sys.argv[1] == 'run':

    ee.addstrategy(enular.strategies.MAcrossover)

    ee.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

    start_portfolio_value = ee.broker.getvalue()

    results = ee.run()

    end_portfolio_value = ee.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    #ee.quantstats(results)
    ee.plot()

if __name__ == '__main__' and sys.argv[1] == 'optimise':

    ee.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')

    ee.optstrategy(enular.strategies.MAcrossover, pfast=range(5, 25), pslow=range(50, 100))

    optimized_runs = ee.run()

    final_results_list = []
    for run in optimized_runs:
        for strategy in run:
            PnL = round(strategy.broker.get_value() - 10000,2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.pfast, 
                strategy.params.pslow, PnL, sharpe['sharperatio']])

    sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3], 
                             reverse=True)
    
    for line in sort_by_sharpe[:5]:
        print(line)

if __name__ == '__main__' and sys.argv[1] == 'screen':
    
    instruments = ['AAPL', 'MSFT', 'GE', 'GRPN']
    
    for ticker in instruments:
        data = enular.YahooData(dataname=ticker, fromdate=datetime(2017, 1, 1), todate=datetime(2022, 1, 1))
        ee.adddata(data)

    ee.addanalyzer(enular.Screener_SMA)
    
    ee.run(runonce=False, stdstats=False, writer=True)