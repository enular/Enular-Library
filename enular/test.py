

import yahoo_fin.stock_info as si
import backtrader as bt

class St(bt.Strategy):

    def __init__(self):

        bt.ind.HullMovingAverage(self.data, _movav=bt.ind.SMMA)







data = bt.feeds.PandasData(dataname=si.get_data
        ("TSLA", start_date="01/01/2017", end_date="01/01/2019",
        index_as_date = True, interval="1d"))


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot()
