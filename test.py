
import backtrader as bt
import yahoo_fin.stock_info as si
# from Moving_Averages import SMA, EMA, DoubleEMA, WMA, HMA, DMA, KAMA, TripleEMA, ZeroLagEMA, TMA
#from MACD import MACD, MACDHisto
#from .enular.indicators import MACDHisto
import enular

class St(bt.Strategy):

    def __init__(self):
        # SMA(self.data)
        # EMA(self.data)
        # DoubleEMA(self.data)
        # WMA(self.data)
        # TripleEMA(self.data)
        # HMA(self.data)
        # DMA(self.data)
        # KAMA(self.data)
        # ZeroLagEMA(self.data)
        # TMA(self.data)
     #   MACD(self.data)
        enular.indicators.MACDHisto(self.data, m1_period=12, m2_period=30, signal_period=10)
        # bt.ind.MACD(self.data)
        # bt.ind.MACDHisto(self.data)


data = bt.feeds.PandasData(dataname=si.get_data
        ("TSLA", start_date="01/01/2017", end_date="01/01/2019",
        index_as_date = True, interval="1d"))

cerebro = enular.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot()
