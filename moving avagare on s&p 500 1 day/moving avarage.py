import os , sys , argparse
import pandas as pd
import backtrader as bt
from goldenstrategy import GoldenCrossover



cerebro = bt.Cerebro()
cerebro.broker.setcash(10000)
spy_prices = pd.read_csv('SPY.csv',index_col='Date',parse_dates=True)

feed = bt.feeds.PandasData( dataname = spy_prices)
cerebro.adddata(feed)
cerebro.addstrategy(GoldenCrossover)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()