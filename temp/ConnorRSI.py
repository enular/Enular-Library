

import backtrader as bt
import yfinance as yf
import quantstats
# import yahoo_fin.stock_info as si


class Streak(bt.Indicator):

    lines = ('streak', )
    params = dict(period=2)

    curstreak = 0

    def next(self):
        current_day, previous_day = self.data[0], self.data[-1]

        if current_day > previous_day:
            self.lines.streak[0] = self.curstreak = max(1, self.curstreak + 1)
        elif current_day < previous_day:
            self.lines.streak[0] = self.curstreak = min(-1, self.curstreak - 1)
        else:
            self.lines.streak[0] = self.curstreak = 0

class ConnorsRSI(bt.Indicator):

    lines = ('crsi', )
    params = dict(prsi=3, pstreak=2, prank=100)

    def __init__(self):

        rsi = bt.indicators.RSI(self.data, period=self.params.prsi)

        streak = Streak(self.data)
        rsi_streak = bt.indicators.RSI(streak, period=self.params.pstreak)

        prank = bt.indicators.PercentRank(self.data, period=self.params.prank)

        self.lines.crsi = (rsi + rsi_streak + prank) / 3.0

class Strategy(bt.Strategy):

    def __init__(self):

        self.connors_indicator = ConnorsRSI()

    def next(self):

        crsi_indicator = self.connors_indicator.lines.crsi[0]
        oversold_threshold = 5
        overbought_threshold = 60
        buy_signal = crsi_indicator < oversold_threshold
        sell_signal = crsi_indicator > overbought_threshold

        if buy_signal:
            print(f'BUY: {crsi_indicator}')
            self.buy()

        if sell_signal:
            print(f'SELL: {crsi_indicator}')
            self.sell()



def run():

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0025)

    data = bt.feeds.PandasData(dataname=yf.download
        ('TSLA', '2017-01-01', '2019-01-01'))
    
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    cerebro.addindicator(Streak)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

    start_portfolio_value = cerebro.broker.getvalue()
    results = cerebro.run()
    strat = results[0]
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value

    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    portfolio_stats = strat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)

    quantstats.reports.html(returns, output='stats.html', title='ConnorsRSI')

run()


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
#     cerebro.run()
#     cerebro.plot()

#     streak = Streak(data)
#     streak.plotinfo.plotname = 'streak'

#     print(f'Final value: {cerebro.broker.getvalue()}')

# run()
