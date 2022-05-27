#!/usr/bin/env python
import os
import sys

import requests
import matplotlib
from datetime import datetime
import backtrader as bt
import yfinance as yf
#from screener import *

import enular

# Instantiate Cerebro engine
#cerebro = bt.Cerebro(optreturn=False)
cerebro = enular.Engine()

# Set data parameters and add to Cerebro
#data = bt.feeds.YahooFinanceCSVData(
#    dataname='TSLA.csv',
#    fromdate=datetime.datetime(2016, 1, 1),
#    todate=datetime.datetime(2021, 12, 25),
#)

#data = bt.feeds.PandasData(dataname=yf.download('TSLA','2017-01-01','2019-01-01'))

data = enular.YahooFinanceData(dataname='TSLA', fromdate=datetime
        (2017, 1, 1), todate=datetime(2019, 1, 1))

# settings for out-of-sample data
# fromdate=datetime.datetime(2018, 1, 1),
# todate=datetime.datetime(2019, 12, 25))

#Add data to Cerebro
#instruments = ['TSLA', 'AAPL', 'GE', 'GRPN']
#for ticker in instruments:
#    data = bt.feeds.YahooFinanceCSVData(
#        dataname='{}.csv'.format(ticker),
#        fromdate=datetime.datetime(2016, 1, 1),
#        todate=datetime.datetime(2017, 10, 30))
#    cerebro.adddata(data) 

#cerebro.addanalyzer(Screener_SMA)

cerebro.adddata(data)

# Add strategy to Cerebro
#cerebro.addstrategy(MAcrossover)


# Default position size
#cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__' and sys.argv[1] == 'test':
    cerebro.run()
    cerebro.plot()


if __name__ == '__main__' and sys.argv[1] == 'run':

    cerebro.addstrategy(enular.MAcrossover)

    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    cerebro.plot()

if __name__ == '__main__' and sys.argv[1] == 'optimise':

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.optstrategy(MAcrossover, pfast=range(5, 10), pslow=range(50, 60))

    optimized_runs = cerebro.run()

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
    #Run Cerebro Engine
    cerebro.run(runonce=False, stdstats=False, writer=True)