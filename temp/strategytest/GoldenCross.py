

import backtrader as bt
import datetime as datetime

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), )

    def __init__(self):
        self.crossovers = []

        for d in self.datas:
            self.fast_moving_average = bt.indicators.SMA(d, period=self.p.fast, plotname='50 day moving average')
            self.slow_moving_average = bt.indicators.SMA(d, period=self.p.slow, plotname='200 day moving average')
            self.crossovers.append(bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average))

    def next(self):
        for i, d in enumerate(self.datas):
            if not self.getpositions(d).size:
                if self.crossovers[i] > 0:
                    self.buy(data = d)

            elif self.crossovers[i] < 0:
                self.close(data = d)

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.broker.set_slippage_perc(perc=0.001)

    stocks = ['APPL', 'TSLA', 'MSFT', 'AMZN']
    for ticker in stocks:
        data = bt.feeds.YahooFinanceData(dataname = 'ticker', fromdate = datetime(2016,1,1), todate = datetime(2018,1,1))
    cerebro.adddata(data, name = 'ticker')

    cerebro.addstrategy(GoldenCross)

    initial_value = cerebro.broker.getvalue()
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    cerebro.plot()