
import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as btfeed
from emacrossoveratrstrategyOnlyBuyside import EmaCrossover
import backtrader.analyzers as btanalyzers

from analyzer_in_dataframe01 import BarAnalysis







# feed = bt.feeds.PandasData( dataname = nse_prices)
# ✨✨✨🐱‍🏍🐱‍🏍
feed = bt.feeds.GenericCSVData(
# downtrend data
# dataname='./Downtrend[5_minute_nifty_50]_01april_22to_14_jul_22.csv',
# dataname='./Downtrend[5_minute_nifty_50]_17_jan_22_to_7march_22.csv',
# dataname='./Downtrend[5_minute_nifty_50]_18_OCT_22_to_21DEC_22.csv',

# uprend data
# dataname='./Uptrend[5_minute_nifty_50]_04_jan_21_to_18_oct_21.csv',
# dataname='./uptrend[5_minute_nifty_50]_21_dec_21_to_17_jan_22.csv',
dataname='./uptrend[5_minute_nifty_50]_7_march_22_to_11_april_22.csv',

# overall data
# dataname='./da overall_data_[5_minute_nifty_50]_04_1_21_to_14_7_22.csv',
datetime=0,
fromdate=datetime.datetime(2021, 1, 4),
timeframe=bt.TimeFrame.Minutes,
dtformat=('%Y-%m-%dT%H:%M:%S+0530'),
open=1,
high=2,
low=3,
close=4,
volume=5,
openinterest=-1,
reverse=True)

# ✨✨✨🐱‍🏍🐱‍🏍

cerebro = bt.Cerebro()
cerebro.addstrategy(EmaCrossover)
cerebro.broker.setcash(100000)
cerebro.adddata(feed)
# cerebro.broker.get_leverage(0)
cerebro.broker.setcommission(commission=0.0, margin=0, mult=1.0, commtype=None, percabs=True, stocklike=False, interest=0.0, interest_long=False, leverage=100, automargin=False, name=None)
cerebro.addsizer(bt.sizers.FixedSize,stake = 50)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.run()
# cerebro.addanalyzer(bt.analyzers.BasicTradeStats, filter='all')
# cerebro.addanalyzer(bt.analyzers.BasicTradeStats, filter='long')
# cerebro.addanalyzer(bt.analyzers.BasicTradeStats, filter='short')

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.addanalyzer(bt.analyzers.AnnualReturn)
cerebro.addanalyzer(bt.analyzers.SharpeRatio)
cerebro.addanalyzer(btanalyzers.DrawDown)
cerebro.addanalyzer(btanalyzers.TradeAnalyzer)

# Analyzer
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydraw')
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='mytrade')
cerebro.addanalyzer(BarAnalysis , _name='mybar')

thestrats = cerebro.run()
thestrat = thestrats[0]

print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
print('drawdown:', thestrat.analyzers.mydraw.get_analysis())
print('trade analzer :', thestrat.analyzers.mytrade.get_analysis())

# EmaCrossover.fund_details()


bar_data_in_dataframe = thestrat.analyzers.mybar.get_analysis()
df = pd.DataFrame(bar_data_in_dataframe)
print(df)
# below code is for convertind dataframes in csv files
# df.to_csv("E:\\algo trading\\csv_files\\trade_history_1_9_21_to_14_7_22.csv", index=False)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()