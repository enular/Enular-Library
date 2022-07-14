
import backtrader as bt
import yahoo_fin.stock_info as si
#import quantstats

class StochasticRSIStrategy(bt.Strategy):

    params = dict(period = 14,
                  hold = 10)

    def __init__(self):
        self.holding = dict()
        self.abc = dict()
        for i, d in enumerate(self.datas):
            self.abc[d] = dict()
            self.abc[d]['rsi'] = bt.ind.RSI(d.close, period=self.p.period)
            self.abc[d]['maxrsi'] = bt.ind.Highest(self.abc[d]['rsi'], period=self.p.period)
            self.abc[d]['minrsi'] = bt.ind.Lowest(self.abc[d]['rsi'], period=self.p.period)
            self.abc[d]['sto_rsi'] = ((self.abc[d]['rsi'] - self.abc[d]['minrsi']) / 
                                        (self.abc[d]['maxrsi'] - self.abc[d]['minrsi']))
            
    def next(self):
        for i, d in enumerate(self.datas):
            pos = self.getposition(d)

            if not pos:
                if (self.abc[d]['sto_rsi'][-1] < self.abc[d]['sto_rsi'][0]) and (self.abc[d]['sto_rsi'][0] < 0.2):
                    self.buy(data=d)

                elif (self.abc[d]['sto_rsi'][-1] < self.abc[d]['sto_rsi'][0]) and (self.abc[d]['sto_rsi'][0] > 0.8):
                    self.sell(data=d)

                self.holding[d] = 0

            elif pos:
                self.holding[d] += 1

                if self.holding[d] >= self.p.hold:
                    self.close(data=d)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.justopened:
            print('{} {} Opened: Price {}, Position {}, Commission {}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.price, 2),
                                                round(trade.value, 2),
                                                round(trade.commission, 2)))

        elif trade.isclosed:
            print('{} {} Closed: Price {}, Gross Profit {}, Net Profit {}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.price, 2),
                                                round(trade.pnl, 2),
                                                round(trade.pnlcomm, 2)))

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.broker.set_slippage_perc(perc=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
    cerebro.addstrategy(StochasticRSIStrategy)

    data0 = bt.feeds.PandasData(dataname=si.get_data
       ("TSLA", start_date="01/01/2020", end_date="01/01/2022",
       index_as_date = True, interval="1d"))
    data1 = bt.feeds.PandasData(dataname=si.get_data
        ("AAPL", start_date="01/01/2020", end_date="01/01/2022",
        index_as_date = True, interval="1d"))
    data2 = bt.feeds.PandasData(dataname=si.get_data
        ("AMZN", start_date="01/01/2020", end_date="01/01/2022",
        index_as_date = True, interval="1d"))

    datalist = [(data0, 'Tesla'), (data1, 'Apple'), (data2, 'Amazon'),]
    for i in range(len(datalist)):
        data = datalist[i][0]
        cerebro.adddata(data, name=datalist[i][1])

    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    strat = results[0]
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    portfolio_stats = strat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)
  #  quantstats.reports.html(returns, output='stats.html', title='Test')

    cerebro.plot(style='candlestick')
