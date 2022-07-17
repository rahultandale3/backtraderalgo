
import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as btfeed





cerebro = bt.Cerebro()
cerebro.broker.setcash(300000)



# below code is suitable for getting access to one day chart
# nse_prices = pd.read_csv('..//NSEI - NSEI.csv',index_col='Date',parse_dates=True)
# nse_prices = pd.read_csv('./15minute_nifty_50_04_1_21_to_3_6_22.csv',index_col='Date',parse_dates=True)
# nse_prices = pd.read_csv('./15minute_nifty_50_04_1_21_to_3_6_22.csv', sep=';', encoding='utf-8-sig', parse_dates=['date'], dayfirst=True, index_col='Date')
# nse_prices = pd.read_csv('..//NSEI - NSEI.csv', sep=';', encoding='utf-8-sig', parse_dates=['date'], dayfirst=True, index_col='Date')

# feed = bt.feeds.PandasData( dataname = nse_prices)
# ✨✨✨🐱‍🏍🐱‍🏍
feed = bt.feeds.GenericCSVData(
dataname='./15minute_nifty_50_04_1_21_to_3_6_22.csv',
datetime=0,
fromdate=datetime.datetime(2021, 1, 4),
timeframe=bt.TimeFrame.Minutes,
dtformat=('%Y-%m-%dT%H:%M:%S'),
open=1,
high=2,
low=3,
close=4,
volume=5,
openinterest=-1,
reverse=True)

# ✨✨✨🐱‍🏍🐱‍🏍


# 🤦‍♂️🤦‍♂️🤦‍♂️🤦‍♂️litteraly i was frustated
# feed = btfeed.GenericCSVData(
# '''this method id wrong menthod , dont use '''
#     dataname='./15minute_nifty_50_04_1_21_to_3_6_22.csv',
#
#     fromdate=datetime.datetime(2021, 1, 4),
#     todate=datetime.datetime(2000, 6, 3),
#
#     nullvalue=0.0,
#
#     dtformat=('%Y-%m-%d'),
#     tmformat=('%H:%M:%S'),
#
#     datetime=0,
#     time=1,
#     open=2,
#     high=3,
#     low=4,
#     close=5,
#     volume=6
# )
# 🤦‍♂️🤦‍♂️🤦‍♂️🤦‍♂️

cerebro.adddata(feed)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()