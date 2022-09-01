
import backtrader as bt
import yahoo_fin.stock_info as si
import datetime
from backtrader.indicators import DMA

from backtrader.analyzers.tradelist import TradeList as TradeList
from tabulate import tabulate

class Enular_Strategy_Example(bt.Strategy):

    params = dict(hold = [20, 20, 20],
                  k_period = 14,
                  d_period = 3,
                  p_entry_limit = 0.005,
                  stop_loss = 0.03,
                  take_price = 0.06,
                  valid = 10)

    def __init__(self):
        self.ord = dict()
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
            dt, dn = self.datetime.date(), d._name
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

            if not pos and not self.ord.get(d, None):
                
                if long:

                    p = d.close[0] * (1.0 - self.p.p_entry_limit)
                    stop = p * (1.0 - self.p.stop_loss)
                    take = p * (1.0 + self.p.take_price)
                    valid = datetime.timedelta(self.p.valid)

                    L1 = self.buy(data=d, exectype=bt.Order.Limit,
                                        price=p, valid=valid, transmit=False)
                    
                    L2 = self.sell(data=d, exectype=bt.Order.Stop,
                                        price=stop, transmit=False, parent=L1)

                    L3 = self.sell(data=d, exectype=bt.Order.Limit,
                                        price=take, transmit=True, parent=L1)

                    self.ord[d] = [L1, L2, L3]

                    print('{} {} Long Position: Main {} Stop {} Limit {}'.format(dt,
                                                                  dn,
                                                                  *(x.ref for x in self.ord[d])))

                elif short:

                    p = d.close[0] * (1.0 + self.p.p_entry_limit)
                    stop = p * (1.0 + self.p.stop_loss)
                    take = p * (1.0 - self.p.take_price)
                    valid = datetime.timedelta(self.p.valid)

                    S1 = self.sell(data=d, exectype=bt.Order.Limit,
                                        price=p, valid=valid, transmit=False)

                    S2 = self.buy(data=d, exectype=bt.Order.Stop,
                                        price=stop, transmit=False, parent=S1)

                    S3 = self.buy(data=d, exectype=bt.Order.Limit,
                                        price=take, transmit=True, parent=S1)

                    self.ord[d] = [S1, S2, S3]

                    print('{} {} Short Position: Main {} Stop {} Limit {}'.format(dt,
                                                                  dn,
                                                                  *(x.ref for x in self.ord[d])))
                
                self.holding[d] = 0

            elif pos:
                self.holding[d] += 1

                if close_long:
                    ord = self.close(data=d)
                    self.ord[d].append(ord)
                    self.cancel(self.ord[d][1])
                    print('{} {} Manual Close of Long Position: %K Crossed 40% Threshold. Order Ref: {}'.format(
                                                                dt,
                                                                dn,
                                                                ord.ref))

                elif close_short:
                    ord = self.close(data=d)
                    self.ord[d].append(ord)
                    self.cancel(self.ord[d][1])
                    print('{} {} Manual Close of Short Position: %K Crossed 60% Threshold. Order Ref: {}'.format(
                                                                dt,
                                                                dn,
                                                                ord.ref))

                elif self.holding[d] >= self.p.hold[i]:
                    ord = self.close(data=d)
                    self.ord[d].append(ord)
                    self.cancel(self.ord[d][1])
                    print('{} {} Manual Close: Holding Period Reached. Order Ref: {}'.format(
                                                                dt,
                                                                dn,
                                                                ord.ref))

    def notify_order(self, order):
        if order.status == order.Submitted: return

        dt, dn = self.datetime.date(), order.data._name
        print('{} {} Order {} Status {}'.format(dt, 
                                                dn, 
                                                order.ref, 
                                                order.getstatusname()))

        order_type = ['main', 'stop', 'limit', 'close']

        if not order.alive():
            d_orders = self.ord[order.data]
            order_index = d_orders.index(order)
            d_orders[order_index] = None
            print('-- No longer alive. Type: {}'.format(order_type[order_index]))

            if all(x is None for x in d_orders):
                d_orders[:] = []

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
    cerebro.addanalyzer(TradeList, _name="trade")

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
    thestrat = cerebro.run(tradehistory=True)
    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_value
    pnl = round(pnl, 2)

    trade_list = thestrat[0].analyzers.trade.get_analysis()
    print (tabulate(trade_list, headers="keys"))

    print(f'Initial Portfolio Value: ${initial_value:2f}')
    print(f'Final Portfolio Value: ${final_value:2f}')
    print(f'Profit and Loss: ${pnl:2f}')

    cerebro.plot()