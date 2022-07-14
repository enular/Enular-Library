
import backtrader as bt
import datetime as datetime
import itertools
import argparse


class StochasticRSI(bt.Indicator):

    lines = ('sto_rsi', )
    params = {'period': 14}

    def __init__(self):
        period = self.p.period
        rsi = bt.ind.RSI(self.data, period=period)
        maxrsi = bt.ind.Highest(rsi, period=period)
        minrsi = bt.ind.Lowest(rsi, period=period)
        self.l.sto_rsi = (rsi - minrsi) / (maxrsi - minrsi)

class StochasticRSIStrategy(bt.Strategy):

    params = dict(valid = 4,
              trailpercent = 0.02, )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s: %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.stochastic_rsi_indicator = StochasticRSI()
        self.order = None
        
        if self.position:
            self.tradeid = itertools.cycle([0, 1, 2])
        else:
            self.tradeid = itertools.cycle([0])

    def notify_order(self, order):
        if order.status == order.Accepted:
            if self.LONG:
                self.log('Broker Accepted Limit Order. Status: Pending')
                self.order = order
                return

            elif self.SHORT:
                self.log('Broker Accepted Limit Order. Status: Pending')
                self.order = order
                return

            else: return

        if order.status == order.Expired:
            self.log('Order Expired')
   
        if order.status == order.Completed:
            if order.isbuy():
                if self.LONG:
                    self.log('Long Position Opened at: Asset Price: $%.2f, Position Size: $%.2f, Broker Commission: $%.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))

                else:
                    self.log('Short Position Closed at: Asset Price: $%.2f, Position Size: $%.2f, Broker Commission: $%.2f' %
                        (order.executed.price,
                        (order.executed.price * order.executed.size * -1),
                         order.executed.comm))

            else:
                if self.SHORT:
                    self.log('Short Position Opened at: Asset Price: $%.2f, Position Size: $%.2f, Broker Commission: $%.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))
                
                else:
                    self.log('Long Position Closed at: Asset Price: $%.2f, Position Size: $%.2f, Broker Commission: $%.2f' %
                        (order.executed.price,
                        (order.executed.price * order.executed.size * -1),
                         order.executed.comm))

            self.bar_executed = len(self.datas)

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed: return

        self.log('Gross Profit: $%.2f, Net Profit: $%.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order: return

        self.log('Closing Price: $%.2f' % self.dataclose[0])

        self.LONG = (self.stochastic_rsi_indicator.l.sto_rsi[-1] < self.stochastic_rsi_indicator.l.sto_rsi[0]
                                                                and self.stochastic_rsi_indicator.l.sto_rsi[0] < 0.2)
        self.SHORT = (self.stochastic_rsi_indicator.l.sto_rsi[-1] > self.stochastic_rsi_indicator.l.sto_rsi[0]
                                                                    and self.stochastic_rsi_indicator.l.sto_rsi[0] > 0.8)

        if self.p.valid:   
            valid = self.data.datetime.date(0) + \
            datetime.timedelta(days=self.p.valid)
        else: valid = None

        if self.LONG and not self.position:
            self.curtradeid = next(self.tradeid)
            self.buy(exectype=bt.Order.StopTrailLimit, valid=valid, trailpercent=self.p.trailpercent, tradeid=self.curtradeid)
            self.log('Bid Limit Order Submitted. Closing Price: $%.2f' % self.dataclose[0])

        elif self.SHORT and not self.position:
            self.curtradeid = next(self.tradeid)
            self.sell(exectype=bt.Order.StopTrailLimit, valid=valid, trailpercent=self.p.trailpercent, tradeid=self.curtradeid)
            self.log('Ask Limit Order Submitted. Closing Price: $%.2f' % self.dataclose[0])

        elif self.position and (len(self) >= (self.bar_executed + 10)):
            self.close(tradeid=self.curtradeid)
            

def runstrat():

    cerebro = bt.Cerebro()
  #  kwargs = dict()

    data0 = bt.feeds.YahooFinanceCSVData(dataname='TSLA.csv',
        fromdate=datetime.datetime(2017, 1, 1),
        todate=datetime.datetime(2019, 1, 1))
    cerebro.adddata(data0, name='d0')

    data1 = bt.feeds.YahooFinanceCSVData(dataname='AAPL.csv',
        fromdate=datetime.datetime(2017, 1, 1),
        todate=datetime.datetime(2019, 1, 1))
    cerebro.adddata(data1, name='d1')

    data2 = bt.feeds.YahooFinanceCSVData(dataname='AMZN.csv',
        fromdate=datetime.datetime(2017, 1, 1),
        todate=datetime.datetime(2019, 1, 1))
    cerebro.adddata(data2, name='d2')

    # cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addstrategy(StochasticRSIStrategy) # **eval('dict(' + args.strat + ')'))
    # cerebro.run(runonce=False) # (**eval('dict(' + args.cerebro + ')'))
    # cerebro.plot()
    
    initial_value = cerebro.broker.getvalue()
    cerebro.run(runonce=False)
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    cerebro.plot()


# def parse_args(pargs=None):
#     parser = argparse.ArgumentParser(
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#         description=('Multiple Values and Brackets'))

#     parser.add_argument('--data0', default='TSLA.csv',
#                         required=False, help='Data0 to read in')

#     parser.add_argument('--data1', default='AAPL.csv',
#                         required=False, help='Data1 to read in')

#     parser.add_argument('--data2', default='AMZN.csv',
#                         required=False, help='Data1 to read in')

#     parser.add_argument('--fromdate', required=False, default='2018-01-01',
#                         help='Date in YYYY-MM-DD format')

#     parser.add_argument('--todate', required=False, default='2020-01-01',
#                         help='Date in YYYY-MM-DD format')

#     parser.add_argument('--cerebro', required=False, default='',
#                         metavar='kwargs', help='kwargs in key=value format')

#     parser.add_argument('--broker', required=False, default='',
#                         metavar='kwargs', help='kwargs in key=value format')

#     parser.add_argument('--sizer', required=False, default='',
#                         metavar='kwargs', help='kwargs in key=value format')

#     parser.add_argument('--strat', required=False, default='',
#                         metavar='kwargs', help='kwargs in key=value format')

#     parser.add_argument('--plot', required=False, default='',
#                         nargs='?', const='{}',
#                         metavar='kwargs', help='kwargs in key=value format')

#     return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()