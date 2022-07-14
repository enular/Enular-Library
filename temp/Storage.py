from datetime import datetime
import backtrader as bt


class OverUnderIndicator(bt.Indicator):
    lines = ( 'overunder' , )

    def __init__(self):

        sma1 = bt.ind.SMA(period = 30)
        sma2 = bt.ind.SMA(period = 100)
        sma3 = bt.ind.SMA(period = 200)

        self.l.overunder = bt.Cmp(sma1, sma2) + bt.Cmp(sma1, sma3) - 1.5


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period = 30)
        sma2 = bt.ind.SMA(period = 100)
        sma3 = bt.ind.SMA(period = 200)
        ind = OverUnderIndicator()
        self.signal_add(bt.SIGNAL_LONG, ind)
        

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
cerebro.addsizer(bt.sizers.PercentSizer, percents = 95)

data0 = bt.feeds.YahooFinanceData(dataname='TSLA', fromdate=datetime(2014, 1, 1),
                                  todate=datetime(2019, 12, 31))
cerebro.adddata(data0)

cerebro.run()
cerebro.plot()

# def run():

#     cerebro = bt.Cerebro()
#     cerebro.broker.setcash(100000)
#     cerebro.broker.setcommission(commission=0.0025)
#     print(f'Starting value: {cerebro.broker.getvalue()}')

#     data = bt.feeds.PandasData(dataname=si.get_data
#         ("TSLA", start_date="01/01/2017", end_date="01/01/2019",
#         index_as_date = True, interval="1d"))
    
#     cerebro.adddata(data)
#     cerebro.addstrategy(Strategy)
#     cerebro.addindicator(Streak)
#     cerebro.addsizer(bt.sizers.PercentSizer, percents = 95)
#     cerebro.run()
#     cerebro.plot()

#     streak = Streak(data)
#     streak.plotinfo.plotname = 'streak'

#     print(f'Final value: {cerebro.broker.getvalue()}')

# run()

# def run():

#     cerebro = bt.Cerebro()
#     cerebro.broker.setcash(100000)
#     cerebro.broker.setcommission(commission=0.0025)

#     data = bt.feeds.PandasData(dataname=si.get_data
#         ("TSLA", start_date="01/01/2017", end_date="01/01/2019",
#         index_as_date = True, interval="1d"))
    
#     cerebro.adddata(data)
#     cerebro.addstrategy(Strategy)
#     cerebro.addindicator(Streak)
#     cerebro.addsizer(bt.sizers.PercentSizer, percents = 95)
#     cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

#     start_portfolio_value = cerebro.broker.getvalue()
#     results = cerebro.run()
#     strat = results[0]
#     end_portfolio_value = cerebro.broker.getvalue()
#     pnl = end_portfolio_value - start_portfolio_value

#     print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
#     print(f'Final Portfolio Value: {end_portfolio_value:2f}')
#     print(f'PnL: {pnl:.2f}')

#     portfolio_stats = strat.analyzers.getbyname('PyFolio')
#     returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
#     returns.index = returns.index.tz_convert(None)

#     quantstats.reports.html(returns, output='stats.html', title='StochSMA')

# run()


# class VarComm(bt.CommInfoBase):
    
#     commissions =[0]

#     def _varcomm(self, size, price, pseudoexec):

#         commissions = self.commissions

#         if commissions:
#             comm = commissions[0] * size * price

#         if not pseudoexec:
#             commissions.pop(0)

#         return comm

# commissions.append(0.005)


# datalist = [
#      ('AAPL.csv', 'Apple'), #[0] = Data file, [1] = Data name
#      ('AMZN.csv', 'Amazon'),
#      ('TSLA.csv', 'Tesla'),
#  ]

#Loop through the list adding to cerebro.
# for i in range(len(datalist)):
#     data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
#     cerebro.adddata(data, name=datalist[i][1])

