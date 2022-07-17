import math
import backtrader as bt

class EmaCrossover(bt.Strategy):
    # def fund_details(self , var):
    #     # self.account_fund_list = []
    #     self.var = self.fund_details()
    #     return  self.var


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        dt1 =  self.datas[0].datetime.time(0)
        print('%s, %s , %s' % (dt.isoformat(),dt1.isoformat(), txt))


    params = (('fast', 13),('slow',29),('order_percentage',0.95),('ticker','SPY'),('period',14),('period1',39))


# -----------------------------------------------------------------------------------------------------------------------
    def __init__(self):

        self.fast_mv = bt.indicators.EMA(self.data.close , period=self.params.fast , plotname ='11 days expo moving avarage')

        self.slow_mv = bt.indicators.EMA(self.data.close , period=self.params.slow , plotname ='26 days expo moving avarage')

        self.crossover = bt.indicators.CrossOver(self.fast_mv,self.slow_mv)

        self.rsi = bt.indicators.RSI(self.data.close , period=self.params.period)

        self.atr = bt.indicators.ATR( period= self.params.period1 )

        self.dataclose = self.datas[0].close
        self.order = None
        self.a = 0
        self.buy_signal = 0
        self.sell_signal = 0
        self.account_fund = 0
        self.account_fund_list = []







    def notify_order(self, order):
        if order.status in[order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % self.data.open[0])
            elif order.issell() :
                self.log('SELL EXECUTED, %.2f' % self.data.open[0])
                # if self.open_sl ==1 :
                #     self.log('SELL EXECUTED OPEN, %.2f' % self.data.close[-1])
                #     self.open_sl = 0

                # else:
                #     self.log('SELL EXECUTED, %.2f' % self.data.open[0])


        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        self.account_fund = self.account_fund+ trade.pnl
        self.account_fund_list.append(self.account_fund)
        self.log('account cum profit  %.2f' %(self.account_fund))
        print(self.account_fund_list)
        # self.log('account cum profit  %.2f' %(self.account_fund_list))


# -------------------------------------------------------------------------------------------------------------------

    def next(self):



        # self.log('Close, %.2f' % self.dataclose[0])
        # print(len(self))
        # print(self.order) # this return order details
        # print(self.position) #this return position details

        if self.crossover > 0  and self.rsi >= 60:
            print(len(self))
            self.a = self.a + 1
            self.buy_signal = self.buy_signal + 1
            self.log('signal no , %.2f' % self.a)
            self.log('buy signal num , %.2f' % self.buy_signal)

            self.log('cross over happern and rsi value is , %.2f' % self.rsi[0])
            self.log('Close, %.2f' % self.dataclose[0])


        elif self.crossover < 0 and self.rsi <= 40 :
            print(len(self))
            self.a = self.a + 1
            self.sell_signal = self.sell_signal + 1
            self.log('signal no , %.2f' % self.a)
            self.log('sell signal num , %.2f' % self.sell_signal)

            self.log('cross under happer and rsi value is , %.2f' % self.rsi[0])
            self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        if self.position.size == 0 :
            if self.crossover > 0 and self.rsi >= 60:
                self.log('SIGNAL GOT FOR BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

                # self.sell_price = (self.data.close[0] - self.data.close[0] * 0.025)
                # self.sell_price_tp = (self.data.close[0] + self.data.close[0] * 0.06)
                self.sell_price = (self.data.low[0] - self.atr[0] * 1.1)
                self.sell_price_tp = (self.data.high[0] + self.atr[0] * 15)

                print("your stop loss is {}  and target is  {} ".format(self.sell_price, self.sell_price_tp))


            elif self.crossover < 0 and self.rsi <= 44:
                self.log('SIGNAL GOT FOR SHORT  CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

                # self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025)
                # self.buy_price_tp = (self.data.close[0] - self.data.close[0] * 0.06)
                self.buy_price = (self.data.high[0] + self.atr[0] * 1)
                self.buy_price_tp = (self.data.low[0] - self.atr[0] * 7)
                print("your stop loss is {}  and target is  {} ".format(self.buy_price, self.buy_price_tp))




        elif self.position.size < 0:
            # self.log('Close, %.2f' % self.dataclose[0])
            # print(len(self))
            # print(self.order) # this return order details
            # print(self.position) #this return position details


            if  self.crossover > 0 and self.rsi >= 60:


                self.log(' SHORT EXIT  DONE CROSS OVER HAPPERN, %.2f' % self.dataclose[0])
                self.close()

                self.log('SIGNAL GOT FOR BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()


                # self.sell_price = (self.data.close[0] - self.data.close[0] * 0.025)
                # self.sell_price_tp = (self.data.close[0] + self.data.close[0] * 0.06)
                self.sell_price = (self.data.low[0] - self.atr[0] * 1.1)
                self.sell_price_tp = (self.data.high[0] + self.atr[0] * 15)

                print("your stop loss is {}  and target is  {} ".format(self.sell_price, self.sell_price_tp))


            elif self.data.open[0] >= self.buy_price:
                self.log('SHORT EXIT  STOP LOSS HIT OPEN, %.2f' % self.data.open[0])
                self.close()



            elif self.data.close[0] >= self.buy_price or self.data.high[0]  >= self.buy_price :
                self.log('SHORT EXIT  STOP LOSS HIT CLOSE, %.2f' % self.data.close[0])
                self.close()



            elif self.data.open[0] <= self.buy_price_tp:
                self.log('SHORT EXIT  TARGET HIT OPEN, %.2f' % self.data.open[0])
                self.close()

            elif self.data.close[0] <= self.buy_price_tp or self.data.low[0]  <= self.buy_price_tp  :
                self.log('SHORT EXIT  TARGET HIT CLOSE, %.2f' % self.data.close[0])
                self.close()








        elif self.position.size > 0 :

            if self.crossover < 0 and self.rsi <= 44 :
                self.log('long EXIT  DONE CROSSUNDER HAPPERN, %.2f' % self.dataclose[0])
                self.close()
                self.log('SIGNAL GOT FOR SHORT  CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

                # self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025 )
                # self.buy_price_tp = (self.data.close[0] - self.data.close[0]*0.06)
                self.buy_price = (self.data.high[0] + self.atr[0] * 1)
                self.buy_price_tp = (self.data.low[0] - self.atr[0] * 7)
                print("your stop loss is {}  and target is  {} ".format(self.buy_price , self.buy_price_tp))

            elif self.data.open[0] <= self.sell_price :
                self.log('long EXIT  STOP LOSS HIT OPEN, %.2f' % self.data.close[0])
                self.order = self.sell()


            elif self.data.close[0] <= self.sell_price or self.data.low[0] <= self.sell_price :
                self.log('long EXIT  STOP LOSS HIT CLOSE, %.2f' % self.data.close[0])
                self.order = self.sell()


            elif self.data.open[0] >= self.sell_price_tp:
                self.log('long EXIT  TARGET HIT OPEN, %.2f' % self.data.close[0])
                self.order = self.sell()

            elif self.data.close[0] >= self.sell_price_tp or self.data.high[0]  >= self.sell_price_tp :
                self.log('long EXIT  TARGET HIT CLOSE, %.2f' % self.data.close[0])
                self.order = self.sell()














