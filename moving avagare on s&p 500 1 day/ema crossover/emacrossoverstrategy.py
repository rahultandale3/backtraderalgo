import math
import backtrader as bt

class EmaCrossover(bt.Strategy):

    # params is touple which we store the values of variable
    params = (('fast', 11),('slow',26),('order_percentage',0.95),('ticker','SPY'),('period',14))

    def __init__(self):
        # in this init we created the variable as the storing the perticular conditon
        self.fast_mv = bt.indicators.SMA(self.data.close , period=self.params.fast , plotname ='11 days expo moving avarage')

        self.slow_mv = bt.indicators.SMA(self.data.close , period=self.params.slow , plotname ='26 days expo moving avarage')

        self.crossover = bt.indicators.CrossOver(self.fast_mv,self.slow_mv)

        self.rsi = bt.indicators.RSI(self.data.close , period=self.params.period)

        self.atr = bt.indicators.ATR( period= self.params.period )
        # no need to use crossuncder because work in both cases it save values in 0 or 1 format
        # self.order = None

        # self.crossunder = bt.indicators.CrossOver(self.slow_mv , self.fast_mv)
        # this crossover store 0 or 1 value if crossover happen it store 1 in crossunder happen it store -1
    def next(self):
        # this next check the codditon in each step
        # if posision is zero means no active trade there only that condition buy order will place
        # if self.order :
        #     return
        if self.position.size <= 0 :
            # self .crossover greter than one means which store zero or one value it means crossover happen

            if self.position.size < 0:
                if  self.crossover > 0 and self.rsi >= 60:
                # if  self.crossover > 0 :


                    print("crossunder happen short exit  {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                                       self.data.close[0]))
                    self.close()
                    # as per the above perams we are utilizing 0.95 money for trading but for safe side we should use only 0.50 % on money
                    amount_to_invest = (self.params.order_percentage * self.broker.cash)
                    # calcutaing the how much quntity we can purchase in that ammount
                    self.size = math.floor(amount_to_invest / self.data.close)

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    print("BUY {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.close[0]))
                    # output of above print Sell 81 SHARES OF SPY AT 118.239998
                    # BUY 87 SHARES OF SPY AT 110.0
                    self.buy(size=self.size)
                    # self.order = self.buy(size=self.size)
                    # self.sell_price = (self.data.close[0] - self.data.close[0]*0.006) 100 rs sl
                    self.sell_price = (self.data.close[0] - self.data.close[0] * 0.025)
                    self.sell_price_tp = (self.data.close[0] + self.data.close[0] * 0.06)

                    print("your stop loss is {}  and target is  {} ".format(self.sell_price, self.sell_price_tp))


                elif self.data.open[0] >= self.buy_price:
                    print("open stop loss short {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                              self.data.open[0]))
                    self.close()

                elif self.data.close[0] >= self.sell_price:
                    print("close stop loss short  {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                                self.data.close[0]))
                    self.close()

                elif self.data.open[0] <= self.sell_price_tp:
                    print(
                        "open target short  {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.open[0]))
                    self.close()

                elif self.data.close[0] <= self.sell_price_tp:
                    print(" close target short {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                             self.data.close[0]))
                    self.close()

            else:
                if self.crossover > 0 and self.rsi >= 60:
                # if self.crossover > 0 :

                    # as per the above perams we are utilizing 0.95 money for trading but for safe side we should use only 0.50 % on money
                    amount_to_invest = (self.params.order_percentage*self.broker.cash)
                    # calcutaing the how much quntity we can purchase in that ammount
                    self.size = math.floor(amount_to_invest/self.data.close)

                    print("BUY {} SHARES OF {} AT {}".format(self.size , self.params.ticker , self.data.close[0]))
                    # output of above print Sell 81 SHARES OF SPY AT 118.239998
                    # BUY 87 SHARES OF SPY AT 110.0
                    self.buy(size=self.size)
                    # self.order = self.buy(size=self.size)
                    # self.sell_price = (self.data.close[0] - self.data.close[0]*0.006) 100 rs sl
                    self.sell_price = (self.data.close[0] - self.data.close[0]*0.025)
                    self.sell_price_tp = (self.data.close[0] + self.data.close[0]*0.06)

                    print("your stop loss is {}  and target is  {} ".format(self.sell_price , self.sell_price_tp))




        elif self.position.size >= 0:
            if self.position.size > 0 :
                if self.crossover < 0 and self.rsi < 40 :
                # if self.crossover < 0 :
                    # as per the above perams we are utilizing 0.95 money for trading but for safe side we should use only 0.50 % on money
                    print("crossunder happen  {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                            self.data.close[0]))
                    self.close()
                    amount_to_invest = (self.params.order_percentage*self.broker.cash)
                    # calcutaing the how much quntity we can purchase in that ammount
                    self.size = math.floor(amount_to_invest/self.data.close)

                    print("sell {} SHARES OF {} AT {}".format(self.size , self.params.ticker , self.data.close[0]))
                    # output of above print Sell 81 SHARES OF SPY AT 118.239998
                    # BUY 87 SHARES OF SPY AT 110.0
                    self.sell(size=self.size)
                    # self.order = self.sell(size=self.size)
                    # self.sell_price = (self.data.close[0] - self.data.close[0]*0.006) 100 rs sl

                    self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025 )
                    self.buy_price_tp = (self.data.close[0] - self.data.close[0]*0.06)

                    print("your stop loss is {}  and target is  {} ".format(self.buy_price , self.buy_price_tp))
                elif self.data.open[0] <= self.sell_price:
                    print(
                        "open stop loss {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.open[0]))
                    self.close()

                elif self.data.close[0] <= self.sell_price:
                    print("close stop loss {} SHARES OF {} AT {}".format(self.size, self.params.ticker,
                                                                         self.data.close[0]))
                    self.close()

                elif self.data.open[0] >= self.sell_price_tp:
                    print("open target  {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.open[0]))
                    self.close()

                elif self.data.close[0] >= self.sell_price_tp:
                    print(
                        " close target {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.close[0]))
                    self.close()


            else:
                if self.crossover < 0 and self.rsi < 40:
                # if self.crossover < 0 :
                    # as per the above perams we are utilizing 0.95 money for trading but for safe side we should use only 0.50 % on money

                    amount_to_invest = (self.params.order_percentage * self.broker.cash)
                    # calcutaing the how much quntity we can purchase in that ammount
                    self.size = math.floor(amount_to_invest / self.data.close)

                    print("sell {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.close[0]))
                    # output of above print Sell 81 SHARES OF SPY AT 118.239998
                    # BUY 87 SHARES OF SPY AT 110.0
                    self.sell(size=self.size)
                    # self.order = self.sell(size=self.size)

                    # self.sell_price = (self.data.close[0] - self.data.close[0]*0.006) 100 rs sl

                    self.buy_price = (self.data.close[0] + self.data.close[0] * 0.025)
                    self.buy_price_tp = (self.data.close[0] - self.data.close[0] * 0.06)









