import math
import backtrader as bt

class EmaCrossover(bt.Strategy):


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    params = (('fast', 11),('slow',26),('order_percentage',0.95),('ticker','SPY'),('period',14))


# -----------------------------------------------------------------------------------------------------------------------
    def __init__(self):

        self.fast_mv = bt.indicators.SMA(self.data.close , period=self.params.fast , plotname ='11 days expo moving avarage')

        self.slow_mv = bt.indicators.SMA(self.data.close , period=self.params.slow , plotname ='26 days expo moving avarage')

        self.crossover = bt.indicators.CrossOver(self.fast_mv,self.slow_mv)

        self.rsi = bt.indicators.RSI(self.data.close , period=self.params.period)

        self.atr = bt.indicators.ATR( period= self.params.period )

        self.dataclose = self.datas[0].close
        self.order = None




    def notify_order(self, order):
        if order.status in[order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():

                self.log('BUY EXECUTED, %.2f' % self.data.open[0])
            elif order.issell() :

                self.log('SELL EXECUTED, %.2f' % self.data.open[0])


        self.order = None

# -------------------------------------------------------------------------------------------------------------------

    def next(self):



        # self.log('Close, %.2f' % self.dataclose[0])
        # print(len(self))
        # print(self.order) # this return order details
        # print(self.position) #this return position details

        if self.crossover > 0  and self.rsi >= 60:
            print(len(self))
            self.log('cross over happern and rsi value is , %.2f' % self.rsi[0])
            self.log('Close, %.2f' % self.dataclose[0])
        elif self.crossover < 0 and self.rsi <= 40 :
            print(len(self))
            self.log('cross under happer and rsi value is , %.2f' % self.rsi[0])
            self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if self.position.size == 0 :
            if self.crossover > 0 and self.rsi >= 60:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

                self.sell_price = (self.data.close[0] - self.data.close[0] * 0.025)
                self.sell_price_tp = (self.data.close[0] + self.data.close[0] * 0.06)

                print("your stop loss is {}  and target is  {} ".format(self.sell_price, self.sell_price_tp))


            elif self.crossover < 0 and self.rsi <= 40:
                self.log('SHORT  CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

                self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025)
                self.buy_price_tp = (self.data.close[0] - self.data.close[0] * 0.06)
                print("your stop loss is {}  and target is  {} ".format(self.buy_price, self.buy_price_tp))




        if self.position.size < 0:
            # self.log('Close, %.2f' % self.dataclose[0])
            # print(len(self))
            # print(self.order) # this return order details
            # print(self.position) #this return position details


            if  self.crossover > 0 and self.rsi >= 60:


                self.log(' SHORT EXIT  DONE CROSS OVER HAPPERN, %.2f' % self.dataclose[0])
                self.close()

                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()


                self.sell_price = (self.data.close[0] - self.data.close[0] * 0.025)
                self.sell_price_tp = (self.data.close[0] + self.data.close[0] * 0.06)

                print("your stop loss is {}  and target is  {} ".format(self.sell_price, self.sell_price_tp))


            elif self.data.open[0] >= self.buy_price:
                self.log('SHORT EXIT  STOP LOSS HIT OPEN, %.2f' % self.data.open[0])
                self.close()


            elif self.data.close[0] >= self.buy_price:
                self.log('SHORT EXIT  STOP LOSS HIT CLOSE, %.2f' % self.data.close[0])
                self.close()


            elif self.data.open[0] <= self.buy_price_tp:
                self.log('SHORT EXIT  TARGET HIT OPEN, %.2f' % self.data.open[0])
                self.close()

            elif self.data.close[0] <= self.buy_price_tp:
                self.log('SHORT EXIT  TARGET HIT CLOSE, %.2f' % self.data.close[0])
                self.close()








        if self.position.size > 0 :

            if self.crossover < 0 and self.rsi <= 40 :
                self.log('long EXIT  DONE CROSSUNDER HAPPERN, %.2f' % self.dataclose[0])
                self.close()
                self.log('SHORT  CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

                self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025 )
                self.buy_price_tp = (self.data.close[0] - self.data.close[0]*0.06)
                print("your stop loss is {}  and target is  {} ".format(self.buy_price , self.buy_price_tp))

            elif self.data.open[0] <= self.sell_price:
                self.log('long EXIT  STOP LOSS HIT OPEN, %.2f' % self.data.close[0])
                self.order = self.sell()

            elif self.data.close[0] <= self.sell_price:
                self.log('long EXIT  STOP LOSS HIT CLOSE, %.2f' % self.data.close[0])
                self.order = self.sell()

            elif self.data.open[0] >= self.sell_price_tp:
                self.log('long EXIT  TARGET HIT OPEN, %.2f' % self.data.close[0])
                self.order = self.sell()

            elif self.data.close[0] >= self.sell_price_tp:
                self.log('long EXIT  TARGET HIT CLOSE, %.2f' % self.data.close[0])
                self.order = self.sell()














