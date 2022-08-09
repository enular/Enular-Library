import numpy as np
import sys
import re
import pickle
import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay #business days
from bisect import bisect
#from tabulate import tabulate

#MACHINE LEARNING MODULES

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression


#YFINANCE REFERENCE
'''
YFINANCE REFERENCE

ticker = yf.Ticker("stock_code")

ticker.info
returns:
'sector': 'Technology',
'fullTimeEmployees': 144000, 
'state': 'WA', 
'country': 'United States', 
'industry': 'Software—Infrastructure', 
'previousClose': 184.68, 
'regularMarketOpen': 184.98, 
'twoHundredDayAverage': 160.92654, 
'trailingAnnualDividendYield': 0.010775396, 
'payoutRatio': 0.3233, 
'volume24Hr': None, 
'regularMarketDayHigh': 185.01, 
'navPrice': None, 
'averageDailyVolume10Day': 32985950,
'totalAssets': None, 
'regularMarketPreviousClose': 184.68, 
'fiftyDayAverage': 167.34735, 
'trailingAnnualDividendRate': 1.99, 
'open': 184.98, 
'averageVolume10days': 32985950, 
'dividendRate': 2.04, 
'beta': 0.952031, 
'regularMarketDayLow': 182.85, 
'priceHint': 2, 
'currency': 'USD', 
'trailingPE': 30.807232, 
'regularMarketVolume': 5037493, 
'marketCap': 1402215989248, 
'averageVolume': 56131512, 
'priceToSalesTrailing12Months': 10.109777, 
'dayLow': 182.85, 
'ask': 183.65, 
'volume': 5037493, 
'fiftyTwoWeekHigh': 190.7, 
'forwardPE': 29.775362, 
'fiveYearAvgDividendYield': 1.95, 
'fiftyTwoWeekLow': 119.01, 
'bid': 183.64, 
'dividendYield': 0.011, 
'bidSize': 2900, 
'dayHigh': 185.01, 
'exchange': 'NMS', 
'exchangeTimezoneName': 'America/New_York', 
'exchangeTimezoneShortName': 'EDT', 
'gmtOffSetMilliseconds': '-14400000', 
'quoteType': 'EQUITY', 
'symbol': 'MSFT', 
'market': 'us_market', 
'enterpriseToRevenue': 9.711, 
'beta3Year': None, 
'profitMargins': 0.33356997, 
'enterpriseToEbitda': 21.015, 
'52WeekChange': 0.497203, 
'morningStarRiskRating': None, 
'forwardEps': 6.21, 
'revenueQuarterlyGrowth': None, 
'sharesOutstanding': 7583439872, 
'bookValue': 15.086, 
'sharesShort': 53310482, 
'sharesPercentSharesOut': 0.0069999998, 
'lastFiscalYearEnd': 1561852800, 
'heldPercentInstitutions': 0.74093, 
'netIncomeToCommon': 46265999360, 
'trailingEps': 6.002, 
'lastDividendValue': None, 
'SandP52WeekChange': 0.041940093, 
'priceToBook': 12.256396, 
'heldPercentInsiders': 0.014249999, 
'nextFiscalYearEnd': 1625011200, 
'mostRecentQuarter': 1585612800, 
'shortRatio': 0.82, 
'sharesShortPreviousMonthDate': 1584057600, 
'floatShares': 7472418682, 
'enterpriseValue': 1346892726272, 
'threeYearAverageReturn': None, 
'lastSplitDate': 1045526400, 
'lastSplitFactor': '2:1', 
'morningStarOverallRating': None, 
'earningsQuarterlyGrowth': 0.221, 
'dateShortInterest': 1586908800, 
'pegRatio': 2.02, 
'shortPercentOfFloat': 0.0070999996, 
'sharesShortPriorMonth': 55155176, 
'regularMarketPrice': 184.98,
}

ticker.history(period="max")
returns:
{
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.
}
'''

#DEFINE FUNCTIONS

def get_intraday_dataset(stock_code):
    ticker = yf.Ticker(stock_code)
    dataset = ticker.history(period=number_of_training_days, interval=intraday_interval)['Open'].values
    return dataset

def get_intraday_volume_dataset(stock_code):
    ticker = yf.Ticker(stock_code)
    dataset = ticker.history(period=number_of_training_days, interval=intraday_interval)['Volume'].values
    return dataset

def categorise(fl, breakpoints=[0], cat=[0,1]):
    return cat[bisect(breakpoints, fl)]

def produce_binary_training_data(dataset):
    X = []
    y = []

    for i in np.arange(ticks_target_ahead + ticks_before_current, dataset.size):
        
        current_index = i - ticks_target_ahead
        start_index = current_index - ticks_before_current
        
        target_price = dataset[i]
        current_price = dataset[current_index]
        change = target_price - current_price
        target = categorise(change)

        training_for_sample = dataset[start_index:current_index + 1]

        X.append(training_for_sample.tolist())
        y.append(target)

    return np.asarray(X), np.asarray(y)

def buy_stock(stock_code):
    ticker = yf.Ticker(stock_code)
    stock_price = ticker.history(start=todays_date)['Open'].values[0]
    return stock_price

def sell_stock(stock_code):
    ticker = yf.Ticker(stock_code)
    stock_price = ticker.history(start=todays_date)['Open'].values[0]
    return stock_price

def test_function(stock_code):
    print(1)

###START OF THE SCRIPT###

#DEFINE VARIABLES

number_of_trades = 10
number_of_training_days = '7d'
intraday_interval = '1m'
number_of_epochs = 1
ticks_target_ahead = 5
ticks_before_current = 30

training_list = ['TSLA']
target_list = ['AAPL']

todays_date = pd.datetime.today()

#RUN SCRIPT

X,y = produce_binary_training_data(dataset=get_intraday_dataset('SHOP'))

print(X.shape)
print(y.shape)

'''
z = np.arange(50)
print(z[0:5])
print(z[5:10])
'''

X_train = X[0:2000,:]
X_test = X[2000:,:]
y_train = y[0:2000]
y_test = y[2000:]

svc = svm.SVC()
rfc = RandomForestClassifier()
gnb = GaussianNB()
knn = KNeighborsClassifier()
dtc = DecisionTreeClassifier()

svc.fit(X_train, y_train)
rfc.fit(X_train, y_train)
gnb.fit(X_train, y_train)
knn.fit(X_train, y_train)
dtc.fit(X_train, y_train)

svc_pred = svc.predict(X_test)
rfc_pred = rfc.predict(X_test)
gnb_pred = gnb.predict(X_test)
knn_pred = knn.predict(X_test)
dtc_pred = dtc.predict(X_test)

#print(confusion_matrix(y_test,y_pred))
#print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, svc_pred))
print(accuracy_score(y_test, rfc_pred))
print(accuracy_score(y_test, gnb_pred))
print(accuracy_score(y_test, knn_pred))
print(accuracy_score(y_test, dtc_pred))
