
import backtrader as bt
import yahoo_fin.stock_info as si
import datetime as datetime

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

    params = (('valid', 4),
              ('trailpercent', 0.02), )

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('%s: %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.stochastic_rsi_indicator = StochasticRSI()
        self.order = None

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
            self.buy(exectype=bt.Order.StopTrailLimit, valid=valid, trailpercent=self.p.trailpercent)
            self.log('Bid Limit Order Submitted. Closing Price: $%.2f' % self.dataclose[0])

        elif self.SHORT and not self.position:
            self.sell(exectype=bt.Order.StopTrailLimit, valid=valid, trailpercent=self.p.trailpercent)
            self.log('Ask Limit Order Submitted. Closing Price: $%.2f' % self.dataclose[0])

        elif self.position and (len(self) >= (self.bar_executed + 10)):
            self.close()

    def notify_order(self, order):
        if order.status in [order.Accepted]:
            if self.LONG or self.SHORT:
                self.log('Order Accepted')
                self.order = order
                return
            
            else: return

        if order.status in [order.Expired]:
            self.log('Order Expired')
   
        if order.status in [order.Completed]:
            if order.isbuy():
                if self.LONG:
                    self.log('Opening Long Position. Target Price: $%.2f, Position Size: $%.2f' %
                        (order.executed.price,
                         order.executed.value))

                else:
                    self.log('Closing Short Position. Target Price: $%.2f' %
                        (order.executed.price))

            else:
                if self.SHORT:
                    self.log('Opening Short Position. Target Price: $%.2f, Position Size: $%.2f' %
                        (order.executed.price,
                         order.executed.value))
                
                else:
                    self.log('Closing Long Position: Target Price: $%.2f' %
                        (order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def notify_trade(self, trade):
        if trade.justopened:
            self.log('Trade Opened at: Asset Price: $%.2f, Position Size: $%.2f, Broker Commission: $%.2f' % 
                    (trade.price, trade.value, trade.commission))
                    
        elif trade.isclosed:
            self.log('Trade Closed at: $%.2f, Gross Profit: $%.2f, Net Profit: $%.2f' %
                    (trade.price, trade.pnl, trade.pnlcomm))
            
if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.broker.set_slippage_perc(perc=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    data = bt.feeds.PandasData(dataname=si.get_data
        ("TSLA", start_date="01/01/2018", end_date="01/01/2019",
        index_as_date = True, interval="1d"))
    
    cerebro.adddata(data)
    cerebro.addstrategy(StochasticRSIStrategy)

    initial_value = cerebro.broker.getvalue()
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    cerebro.plot()