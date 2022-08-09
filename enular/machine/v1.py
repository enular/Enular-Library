import numpy as np
import sys
import re
import pickle
import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BDay
from bisect import bisect
from tabulate import tabulate

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression

'''
YFINANCE REFERENCE

msft = yf.Ticker("MSFT")

msft.info
returns:
{'zip': '98052',
'sector': 'Technology',
'fullTimeEmployees': 144000, 
'longBusinessSummary': 'Microsoft Corporation develops, 
'city': 'Redmond', 
'phone': '425-882-8080', 
'state': 'WA', 
'country': 'United States', 
'companyOfficers': [], 
'website': 'http://www.microsoft.com', 
'maxAge': 1, 'address1': 'One Microsoft Way', '
fax': '425-706-7329', 
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
'toCurrency': None, 
'averageVolume10days': 32985950, 
'expireDate': None, 
'yield': None, 
'algorithm': None, 
'dividendRate': 2.04, 
'exDividendDate': 1589932800, 
'beta': 0.952031, 
'circulatingSupply': None, 
'startDate': None, 
'regularMarketDayLow': 182.85, 
'priceHint': 2, 
'currency': 'USD', 
'trailingPE': 30.807232, 
'regularMarketVolume': 5037493, 
'lastMarket': None, 
'maxSupply': None, 
'openInterest': None, 
'marketCap': 1402215989248, 
'volumeAllCurrencies': None, 
'strikePrice': None, 
'averageVolume': 56131512, 
'priceToSalesTrailing12Months': 10.109777, 
'dayLow': 182.85, 
'ask': 183.65, 
'ytdReturn': None, 
'askSize': 1100, 
'volume': 5037493, 
'fiftyTwoWeekHigh': 190.7, 
'forwardPE': 29.775362, 
'fromCurrency': None, 
'fiveYearAvgDividendYield': 1.95, 
'fiftyTwoWeekLow': 119.01, 
'bid': 183.64, 
'tradeable': False, 
'dividendYield': 0.011, 
'bidSize': 2900, 
'dayHigh': 185.01, 
'exchange': 'NMS', 
'shortName': 'Microsoft Corporation', 
'longName': 'Microsoft Corporation', 
'exchangeTimezoneName': 'America/New_York', 
'exchangeTimezoneShortName': 'EDT', 
'isEsgPopulated': False, 
'gmtOffSetMilliseconds': '-14400000', 
'quoteType': 'EQUITY', 
'symbol': 'MSFT', 
'messageBoardId': 'finmb_21835', 
'market': 'us_market', 
'annualHoldingsTurnover': None, 
'enterpriseToRevenue': 9.711, 
'beta3Year': None, 
'profitMargins': 0.33356997, 
'enterpriseToEbitda': 21.015, 
'52WeekChange': 0.497203, 
'morningStarRiskRating': None, 
'forwardEps': 6.21, 
'revenueQuarterlyGrowth': None, 
'sharesOutstanding': 7583439872, 
'fundInceptionDate': None, 
'annualReportExpenseRatio': None, 
'bookValue': 15.086, 
'sharesShort': 53310482, 
'sharesPercentSharesOut': 0.0069999998, 
'fundFamily': None, 
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
'legalType': None, 
'morningStarOverallRating': None, 
'earningsQuarterlyGrowth': 0.221, 
'dateShortInterest': 1586908800, 
'pegRatio': 2.02, 
'lastCapGain': None, 
'shortPercentOfFloat': 0.0070999996, 
'sharesShortPriorMonth': 55155176, 
'category': None, 
'fiveYearAverageReturn': None, 
'regularMarketPrice': 184.98, 
'logo_url': 'https://logo.clearbit.com/microsoft.com'}

msft.history(period="max")
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
'''

if len(sys.argv) == 1:
    
    print("Enter a command")
    exit()

stocks = ['MSFT','AAPL','AMZN','GOOG','FB','JNJ','V','PG','JPM','INTC']
#targets = ['MSFT','AAPL','AMZN','GOOG','FB','JNJ','V','PG','JPM','INTC']
targets = ['TSLA']


if sys.argv[1] == 'classify':
    
    #def category(fl, breakpoints=[-0.05,-0.04,-0.03,-0.02,-0.01,0,0.01,0.02,0.03,0.04,0.05], cat=[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5]):
    #        return cat[bisect(breakpoints, fl)]
    def category(fl, breakpoints=[-0.03,-0.01,0.01,0.03], cat=[-2,-1,0,1,2]):
            return cat[bisect(breakpoints, fl)]

    X = []
    y = []

    shift = 5 #how many days into the future you would like to predict

    #[1 1 0 1 1 0 1 1 1 1] 5 70%
    #[0 0 -1 0 0 -1 0 0 -1 0] 10 42%
    #[ 0 -1  0  0  0  0 -1  0  1  0] 7 79%

    #testing the classifier only
    #dates = [0,1,2]
    #subdates = [0,1,2]

    #dates = [10,20,40,60,80,100,120,140,160,180,200,220,240] 
    #subdates = [1,2,4,8,16,32,64,128,256] #days before sample date, add 0 to beginning if today

    dates = [1,2,3,4,6,8,12,16,24,32,48,64,96,128,140,160,180,200,220,240]
    subdates = [1,2,3,4,5,6,7,8,10,12,14,16,20,24,28,32,40,48,56,64,80,96,112,128,152,256] #days before sample date, add 0 to beginning if today


    xtarget = []

    for target in targets:

        #initialisation
        stocktarget = yf.Ticker(target)
        xtargetsample = []

        #price of target today
        tdtarget = pd.datetime.today()
        tdoptarget = stocktarget.history(start=tdtarget)['Open'].values[0]
        
        #other features


        #relative price of target for days in the past
        for subdate in subdates:
            subdate = subdate + 1
            tdmtarget = tdtarget - BDay(subdate)
            tdmoptarget = stocktarget.history(start=tdmtarget)['Open'].values[0]
            nchange = (tdmoptarget-tdoptarget)/tdoptarget
            print(nchange)
            xtargetsample.append(nchange)
        xtarget.append(xtargetsample)

    print(xtarget)

    for stockcode in stocks:

        #initialisation
        stock = yf.Ticker(stockcode)

        for date in dates:
            
            date = date + shift
            td = pd.datetime.today() - BDay(date) #target date
            tdop = stock.history(start=td)['Open'].values[0] #target date opening price
            tdpo = td + BDay(shift) #target date plus one
            tdpoop = stock.history(start=tdpo)['Open'].values[0] #target day plus one opening price
            ychange = (tdpoop-tdop)/tdop #percentage change on td
            yclass = category(ychange) #class for ML
            print("Class:" + str(yclass))
            
            xsample = []
            for subdate in subdates:
                subdate = subdate + 1
                tdm = td - BDay(subdate)
                tdmop = stock.history(start=tdm)['Open'].values[0]
                nchange = (tdmop-tdop)/tdop
                print(nchange)
                xsample.append(nchange)

            X.append(xsample)
            y.append(yclass)

    print(X)
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

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

    targetpred = rfc.predict(xtarget)
    print (targetpred)

    #print(inputdata.t2wsarget_names)
    #print (target_pred)

elif sys.argv[1] == 'regress':
    
    X = [[1,2,4],[5,8,6],[16,20,34],[103,264,155],[1056,2341,1445]]
    y = [2,7,16,112,1076]
    test = [[1000,2000,1500]]
    clf = svm.SVR()
    clf.fit(X, y)
    pred = clf.predict(test)
    print(pred)

elif sys.argv[1] == 'analysis':
    
    if len(sys.argv) < 3:
        print('Enter a stock code')
        exit()

    elif len(sys.argv) == 3:
        
        stockcode = sys.argv[2]
        ticker = yf.Ticker(stockcode)

        trailingPE = ''
        try:
            trailingPE = str(ticker.info['trailingPE'])
        except:
            trailingPE = 'No trailing PE'

        table = [('Stock name: ', ticker.info['longName']),
        ('Day low: ', str(ticker.info['dayLow'])),
        ('Day high: ', str(ticker.info['dayHigh'])),
        ('50 day average: ', str(ticker.info['fiftyDayAverage'])),
        ('200 day average: ', str(ticker.info['twoHundredDayAverage'])),
        ('52 week low: ', str(ticker.info['fiftyTwoWeekLow'])),
        ('52 week high: ', str(ticker.info['fiftyTwoWeekHigh'])),
        ('Market cap: ', str(ticker.info['marketCap'])),
        ('Enterprise value: ', str(ticker.info['enterpriseValue'])),
        ('Price to sales: ', str(ticker.info['priceToSalesTrailing12Months'])),
        ('Price to book: ', str(ticker.info['priceToBook'])),
        ('Trailing PE: ', trailingPE),
        ('Forward PE: ', str(ticker.info['forwardPE'])),
        ('PEG ratio: ', str(ticker.info['pegRatio'])),
        ('Short ratio: ', str(ticker.info['shortRatio']))]

        headers = ['Detail', 'Stock']

        print(tabulate(table))

        '''
        print (' ')
        try:
            print ('Stock name: ' + ticker.info['longName'])
        except:
            print ('Stock name: ' + ticker.info['shortName'])
        print ('Day low: ' + str(ticker.info['dayLow']))
        print ('Day high: ' + str(ticker.info['dayHigh']))
        print ('50 day average: ' + str(ticker.info['fiftyDayAverage']))
        print ('200 day average: ' + str(ticker.info['twoHundredDayAverage']))
        print ('52 week low: ' + str(ticker.info['fiftyTwoWeekLow']))
        print ('52 week high: ' + str(ticker.info['fiftyTwoWeekHigh']))
        print ('Market cap: ' + str(ticker.info['marketCap']))
        print ('Enterprise value: ' + str(ticker.info['enterpriseValue']))
        print ('Price to sales: ' + str(ticker.info['priceToSalesTrailing12Months']))
        print ('Price to book: ' + str(ticker.info['priceToBook']))
        try:
            print ('Trailing PE: ' + str(ticker.info['trailingPE']))
        except:
            print ('No trailing PE')
        print ('Forward PE: ' + str(ticker.info['forwardPE']))
        print ('PEG ratio: ' + str(ticker.info['pegRatio']))
        print ('Short ratio: ' + str(ticker.info['shortRatio']))
        '''

    elif len(sys.argv) == 4:
        
        stockcode = sys.argv[2]
        ticker = yf.Ticker(stockcode)

        stockcodecomp = sys.argv[3]
        tickercomp = yf.Ticker(stockcodecomp)

        trailingPE = ''
        try:
            trailingPE = str(ticker.info['trailingPE'])
        except:
            trailingPE = 'No trailing PE'
        trailingPEcomp = ''
        try:
            trailingPEcomp = str(tickercomp.info['trailingPE'])
        except:
            trailingPEcomp = 'No trailing PE'

        table = [('Stock name: ', ticker.info['longName'], tickercomp.info['longName']),
        ('Day low: ', str(ticker.info['dayLow']), str(tickercomp.info['dayLow'])),
        ('Day high: ', str(ticker.info['dayHigh']), str(tickercomp.info['dayHigh'])),
        ('50 day average: ', str(ticker.info['fiftyDayAverage']), str(tickercomp.info['fiftyDayAverage'])),
        ('200 day average: ', str(ticker.info['twoHundredDayAverage']), str(tickercomp.info['twoHundredDayAverage'])),
        ('52 week low: ', str(ticker.info['fiftyTwoWeekLow']), str(tickercomp.info['fiftyTwoWeekLow'])),
        ('52 week high: ', str(ticker.info['fiftyTwoWeekHigh']), str(tickercomp.info['fiftyTwoWeekHigh'])),
        ('Market cap: ', str(ticker.info['marketCap']), str(tickercomp.info['marketCap'])),
        ('Enterprise value: ', str(ticker.info['enterpriseValue']), str(tickercomp.info['enterpriseValue'])),
        ('Price to sales: ', str(ticker.info['priceToSalesTrailing12Months']), str(tickercomp.info['priceToSalesTrailing12Months'])),
        ('Price to book: ', str(ticker.info['priceToBook']), str(tickercomp.info['priceToBook'])),
        ('Trailing PE: ', trailingPE, trailingPEcomp),
        ('Forward PE: ', str(ticker.info['forwardPE']), str(tickercomp.info['forwardPE'])),
        ('PEG ratio: ', str(ticker.info['pegRatio']), str(tickercomp.info['pegRatio'])),
        ('Short ratio: ', str(ticker.info['shortRatio']), str(tickercomp.info['shortRatio']))]

        headers = ['Detail', 'Stock One', 'Stock two']

        print(tabulate(table))

else:
    
    print('Enter a valid command')
    exit()