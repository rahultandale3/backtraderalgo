import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as btfeed
from atrslandtarget import EmaCrossover

# ---------------------------------------------------------------------------------------------
nse_prices = pd.read_csv('./NSEI - NSEI.csv',index_col='Date',parse_dates=True)
feed = bt.feeds.PandasData( dataname = nse_prices)

# ---------------------------------------------------------------------------------------------

cerebro = bt.Cerebro()
cerebro.addstrategy(EmaCrossover)
cerebro.broker.setcash(300000)
# cerebro.addsizer(bt.sizers.FixedSize,stake = 50)
cerebro.adddata(feed)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()