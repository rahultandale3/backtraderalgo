import os , sys , argparse
import pandas as pd
import backtrader as bt
from emacrossoverstrategy import EmaCrossover



cerebro = bt.Cerebro()
cerebro.broker.setcash(300000)
nse_prices = pd.read_csv('../NSEI - NSEI.csv',index_col='Date',parse_dates=True)

feed = bt.feeds.PandasData( dataname = nse_prices)
cerebro.adddata(feed)
cerebro.addstrategy(EmaCrossover)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()