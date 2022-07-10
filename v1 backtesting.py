# video number 3
import backtrader as bt
import pandas as pd
import datetime

import backtesting
import matplotlib
from strategy import TestStrategy #impoting strategy file and its class teststrategy

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000)


# creating datafeeds
# data = bt.feeds.YahooFinanceCSVData(dataname='ohlcdata.csv')
data = bt.feeds.YahooFinanceCSVData(
    dataname= 'RELIANCE.NS.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2001,6, 11),
    # Do not pass values before this date
    todate=datetime.datetime(2022, 6, 8),
    # Do not pass values after this date
    reverse=False)
# it considering 6th colunm as a close value but ohlcdata.csv contain 6th number volume column
# adding data to cerebro
cerebro.adddata(data)


# giving strategy file to cerebro
cerebro.addstrategy(TestStrategy)
# sezer means order quntity
cerebro.addsizer(bt.sizers.FixedSize,stake = 10)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()





