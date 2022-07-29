
import backtrader as bt
import yahoo_fin.stock_info as si
from backtrader.indicators import DMA


class Enular_Strategy_Example(bt.Strategy):

    params = dict(hold = 20,
                  k_period = 14,
                  d_period = 3)

    def __init__(self):
        self.holding = dict()
        self.stoch = dict()
        self.condition = dict()

        for i, d in enumerate(self.datas):
            self.stoch[d] = dict()
            self.condition[d] = dict()
            self.stoch[d]['sto'] = bt.ind.StochasticFast(d, period=self.p.k_period, period_dfast=self.p.d_period, movav=DMA)
            self.stoch[d]['v'] = abs(self.stoch[d]['sto'].lines.percK - self.stoch[d]['sto'].lines.percK(-1))
            self.condition[d]['close_long'] = bt.ind.CrossUp(self.stoch[d]['sto'].lines.percK, 40.0, plot=False)
            self.condition[d]['close_short'] = bt.ind.CrossDown(self.stoch[d]['sto'].lines.percK, 60.0, plot=False)

    def next(self):
        for i, d in enumerate(self.datas):
            pos = self.getposition(d)

            long = self.stoch[d]['v'][0] > self.stoch[d]['v'][-1] and \
                    self.stoch[d]['sto'].lines.percK[0] < 20 and \
                    self.stoch[d]['sto'].lines.percD[0] < 20 and \
                    self.stoch[d]['sto'].lines.percK[0] <= self.stoch[d]['sto'].lines.percD[0]

            close_long = self.condition[d]['close_long'][0]

            short = self.stoch[d]['v'][0] > self.stoch[d]['v'][-1] and \
                    self.stoch[d]['sto'].lines.percK[0] > 80 and \
                    self.stoch[d]['sto'].lines.percD[0] > 80 and \
                    self.stoch[d]['sto'].lines.percK[0] >= self.stoch[d]['sto'].lines.percD[0]

            close_short = self.condition[d]['close_short'][0]

            if not pos:
                if long:
                    self.buy(data=d)

                elif short:
                    self.sell(data=d)
                
                self.holding[d] = 0

            elif pos:
                self.holding[d] += 1
                
                if close_long:
                    self.close(data=d)

                elif close_short:
                    self.close(data=d)

                elif self.holding[d] >= self.p.hold:
                    self.close(data=d)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        
        if trade.justopened:
            print('{} -- {} Opened: Price ${}, Position ${}, Commission ${}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.price, 2),
                                                round(trade.value, 2),
                                                round(trade.commission, 2)))

        elif trade.isclosed:
            print('{} -- {} Closed: Gross Profit ${}, Net Profit ${}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.pnl, 2),
                                                round(trade.pnlcomm, 2)))

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0025)
    cerebro.broker.set_slippage_perc(perc=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=50)
    cerebro.addstrategy(Enular_Strategy_Example)

    data0 = bt.feeds.PandasData(dataname=si.get_data("TSLA",
                                                    start_date="01/01/2020",
                                                    end_date="01/01/2022",
                                                    index_as_date = True,
                                                    interval="1d"))

    data1 = bt.feeds.PandasData(dataname=si.get_data("AAPL",
                                                    start_date="01/01/2020",
                                                    end_date="01/01/2022",
                                                    index_as_date = True,
                                                    interval="1d"))

    data2 = bt.feeds.PandasData(dataname=si.get_data("AMZN",
                                                    start_date="01/01/2020",
                                                    end_date="01/01/2022",
                                                    index_as_date = True,
                                                    interval="1d"))

    datalist = [(data0, 'Tesla'),
                (data1, 'Apple'),
                (data2, 'Amazon')]

    for i in range(len(datalist)):
        data = datalist[i][0]
        cerebro.adddata(data, name=datalist[i][1])

    initial_value = cerebro.broker.getvalue()
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    cerebro.plot()