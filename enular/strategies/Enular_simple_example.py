
import backtrader as bt
import yahoo_fin.stock_info as si
from backtrader.indicators import DMA

class Enular_Strategy_Example(bt.Strategy):

    params = (('hold', 20),
              ('k_period', 14),
              ('d_period', 3), )

    def __init__(self):
        self.holding = ()

        self.stoch = bt.ind.StochasticFast(self.data, period=self.p.k_period, period_dfast=self.p.d_period, movav=DMA)
        self.v1 = abs(self.stoch.lines.percK(-1) - self.stoch.lines.percK(-2))
        self.v2 = abs(self.stoch.lines.percK - self.stoch.lines.percK(-1))
        self.close_long = bt.ind.CrossUp(self.stoch.lines.percK, 40.0, plot=False)
        self.close_short = bt.ind.CrossDown(self.stoch.lines.percK, 60, plot=False)


    def next(self):
        k = self.stoch.lines.percK
        d = self.stoch.lines.percD
        buy_signal = self.v2 > self.v1 and k < 20 and d < 20 and k >= d
        sell_signal = self.v2 > self.v1 and k > 80 and d > 80 and k <= d
        close_long = self.close_long
        close_short = self.close_short

        if not self.position:
            if buy_signal:
                self.buy()

            elif sell_signal:
                self.sell()

            self.holding = 1

        elif self.position:
            self.holding += 1

            if close_long:
                self.close()

            elif close_short:
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