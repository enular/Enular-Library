from __future__ import (absolute_import, division, print_function, unicode_literals)

#!/usr/bin/env python
import os
import io
import sys

from datetime import date, datetime
import matplotlib
import yfinance as yf
import numpy
import scipy
import sklearn
import pandas
import backtrader as bt
import webbrowser
import quantstats

#Dependencies for Yahoo data streamer
from backtrader.utils.py3 import (urlopen, urlquote, ProxyHandler, build_opener, install_opener)
import collections
import itertools
from backtrader import feed
from backtrader.utils import date2num

if __name__ == '__main__':
    print ('Do not run this file.')

#CORE

class Cerebro(bt.Cerebro):  
    
    def quantstats(self, results):
            strat = results[0]
            portfolio_stats = strat.analyzers.getbyname('PyFolio')
            returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
            returns.index = returns.index.tz_convert(None)
            quantstats.reports.html(returns, output='stats.html', title='BTC Sentiment', download_filename='stats.html')
            webbrowser.open('file://' + os.path.realpath('stats.html'))

class Dummy(bt.Indicator):    
    pass

class Indicator(bt.Indicator):
    
    params = (
        ('indicator_a',Dummy),
        ('indicator_b',Dummy),
    )

    plotinfo = dict(subplot=False)

    def trade_logic(self):
        pass

    def __init__(self):

        self.data0 = self.params.indicator_a(self.data)
        self.data1 = self.params.indicator_b(self.data)

        self.trade_logic()

class Strategy(bt.Strategy):
    
    params = (
        ('indicator_a',Dummy),
        ('indicator_b',Dummy),
    )

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None

        self.indicator_a = self.params.indicator_a(self.datas[0])
        self.indicator_b = self.params.indicator_b(self.datas[0])

    def trade_logic(self):
        pass

    def close_logic(self):
        if len(self) >= (self.bar_executed + 5):
            self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
            self.order = self.close()

    def next(self):

        if self.order:
            return

        if not self.position:
            self.trade_logic()

        else:
            self.close_logic()

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') # Comment this line when running optimization

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                (trade.pnl, trade.pnlcomm))

#SECONDARY

class YahooData(bt.feeds.YahooFinanceData):

    def start_v7(self):
        try:
            import requests
        except ImportError:
            msg = ('The new Yahoo data feed requires to have the requests '
                   'module installed. Please use pip install requests or '
                   'the method of your choice')
            raise Exception(msg)

        self.error = None
        url = self.p.urlhist.format(self.p.dataname)

        sesskwargs = dict()
        if self.p.proxies:
            sesskwargs['proxies'] = self.p.proxies

        crumb = None
        sess = requests.Session()
        sess.headers['User-Agent'] = 'backtrader'
        for i in range(self.p.retries + 1):  # at least once
            resp = sess.get(url, **sesskwargs)
            if resp.status_code != requests.codes.ok:
                continue

            txt = resp.text
            i = txt.find('CrumbStore')
            if i == -1:
                continue
            i = txt.find('crumb', i)
            if i == -1:
                continue
            istart = txt.find('"', i + len('crumb') + 1)
            if istart == -1:
                continue
            istart += 1
            iend = txt.find('"', istart)
            if iend == -1:
                continue

            crumb = txt[istart:iend]
            crumb = crumb.encode('ascii').decode('unicode-escape')
            break

        if crumb is None:
            self.error = 'Crumb not found'
            self.f = None
            return

        crumb = urlquote(crumb)

        # urldown/ticker?period1=posix1&period2=posix2&interval=1d&events=history&crumb=crumb

        # Try to download
        urld = '{}/{}'.format(self.p.urldown, self.p.dataname)

        urlargs = []
        posix = date(1970, 1, 1)
        #if self.p.todate is not None:
        #    period2 = (self.p.todate.date() - posix).total_seconds()
        #    urlargs.append('period2={}'.format(int(period2)))

        #if self.p.todate is not None:
        if self.p.fromdate is not None:
            period1 = (self.p.fromdate.date() - posix).total_seconds()
            #urlargs.append('period1={}'.format(int(period1)))
        else:
            period1 = 0
        urlargs.append('period1={}'.format(int(period1)))
        if self.p.todate is not None:
            period2 = (self.p.todate.date() - posix).total_seconds()
        else:
            # use current time as todate if not provided
            period2 = (datetime.utcnow().date() - posix).total_seconds()
        urlargs.append('period2={}'.format(int(period2)))

        intervals = {
            bt.TimeFrame.Days: '1d',
            bt.TimeFrame.Weeks: '1wk',
            bt.TimeFrame.Months: '1mo',
        }

        urlargs.append('interval={}'.format(intervals[self.p.timeframe]))
        urlargs.append('events=history')
        urlargs.append('crumb={}'.format(crumb))

        urld = '{}?{}'.format(urld, '&'.join(urlargs))
        f = None
        for i in range(self.p.retries + 1):  # at least once
            resp = sess.get(urld, **sesskwargs)
            if resp.status_code != requests.codes.ok:
                continue

            ctype = resp.headers['Content-Type']
            # Cover as many text types as possible for Yahoo changes
            if not ctype.startswith('text/'):
                self.error = 'Wrong content type: %s' % ctype
                continue  # HTML returned? wrong url?

            # buffer everything from the socket into a local buffer
            try:
                # r.encoding = 'UTF-8'
                f = io.StringIO(resp.text, newline=None)
            except Exception:
                continue  # try again if possible

            break

        self.f = f

class Order(bt.order.Order):
    pass

class Broker(bt.brokers.BackBroker):
    pass

class Analyzer(bt.Analyzer):
    pass

#TEST

class Test:
    
    a = 1

    def __init__(self):
        self.a = 2
    
    def test_the_test(self):
        print(self.a)

class Train:
    pass