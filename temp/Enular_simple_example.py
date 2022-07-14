
import backtrader as bt
import yahoo_fin.stock_info as si

class Enular_Strategy_Example(bt.Strategy):

    params = (('hold', 20),
              ('k_period', 14),
              ('d_period', 3), )

    def __init__(self):
        self.holding = ()

        highest = bt.ind.Highest(self.data, period=self.p.k_period, plot=False)
        lowest = bt.ind.Lowest(self.data, period=self.p.d_period, plot=False)
        self.k = (self.data - lowest) / (highest - lowest)
        self.d = bt.ind.EMA(self.k, period=self.p.d_period, plot=False)
        self.v1 = abs(self.k(-1) - self.k(-2))
        self.v2 = abs(self.k - self.k(-1))
        bt.ind.StochasticFast(self.data, period=self.p.k_period, period_dfast=self.p.d_period)

    def next(self):
        buy_signal = self.v2 > self.v1 and self.k < 20 and self.d < 20 and self.k >= self.d
        sell_signal = self.v2 > self.v1 and self.k > 80 and self.d > 80 and self.k <= self.d

        if not self.position:
            if buy_signal:
                self.buy()

            elif sell_signal:
                self.sell()

            self.holding = 1

        elif self.position:
            self.holding += 1

            if self.k in range(45, 65):
                self.close()
                
            elif self.holding >= self.p.hold:
                self.close()

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        
        if trade.justopened:
            print('{}: Trade Opened at: ${}, Position: ${}, Commission: ${}'.format(
                                                            dt,
                                                            round(trade.price, 2),
                                                            round(trade.value, 2),
                                                            round(trade.commission, 2)))
                    
        elif trade.isclosed:
            print('{}: Trade Closed. Gross Profit: ${}, Net Profit: ${}'.format(
                                                            dt,
                                                            round(trade.pnl, 2),
                                                            round(trade.pnlcomm, 2)))

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0025)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    data = bt.feeds.PandasData(dataname=si.get_data("TSLA",
                                                    start_date="01/01/2020",
                                                    end_date="01/01/2022",
                                                    index_as_date = True,
                                                    interval="1d"))
    
    cerebro.adddata(data)
    cerebro.addstrategy(Enular_Strategy_Example)

    start_portfolio_value = cerebro.broker.getvalue()
    cerebro.run()
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    pnl = round(pnl, 2)

    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    cerebro.plot()