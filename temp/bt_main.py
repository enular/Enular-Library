import backtrader as bt
from strategies import *
import yahoo_fin.stock_info as si
import quantstats

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

# Set data parameters and add to Cerebro

data1= bt.feeds.PandasData(dataname=si.get_data("tsla", start_date="12/04/2017", end_date="12/04/2019", index_as_date = True, interval="1d"))

cerebro.adddata(data1)

# Add strategy to Cerebro
cerebro.addstrategy(MAcrossover)

# Add commission rate of 0.1% per trade
cerebro.broker.setcommission(commission=0.0025)

# Add analyzers
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

if __name__ == '__main__':

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

	quantstats.reports.html(returns, output='stats.html', title='MAcrossover')