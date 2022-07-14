from yahoo_fin.stock_info import get_data
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn
import statsmodels.tsa.stattools as ts

amazon_weekly= get_data("amzn", start_date="12/04/2017", end_date="12/04/2019", index_as_date = True, interval="1d")

def hurst(ts):

    lags = range(2, 100)

    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    poly = polyfit(log(lags), log(tau), 1)

    return poly[0]*2.0


gbm = log(cumsum(randn(100000))+1000)
mr = log(randn(100000)+1000)
tr = log(cumsum(randn(100000)+1)+1000)

print("Hurst(GBM): %s" % hurst(gbm))
print("Hurst(MR): %s" % hurst(mr))
print("Hurst(TR): %s" % hurst(tr))
print("Hurst(amzn): %s" % hurst(amazon_weekly["close"]))
print("Amazon weekly closing price:\n", amazon_weekly.tail())
print("Augmented Dickey-Fuller:", ts.adfuller(amazon_weekly["close"], 1))