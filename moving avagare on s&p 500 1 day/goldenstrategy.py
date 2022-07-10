import math
import backtrader as bt

class GoldenCrossover(bt.Strategy):
    # params is touple which we store the values of variable
    params = (('fast', 11),('slow',26),('order_percentage',0.95),('ticker','SPY'))

    def __init__(self):
        # in this init we created the variable as the storing the perticular conditon
        self.fast_mv = bt.indicators.SMA(self.data.close , period=self.params.fast , plotname ='50 days moving avarage')

        self.slow_mv = bt.indicators.SMA(self.data.close , period=self.params.slow , plotname ='50 days moving avarage')

        self.crossover = bt.indicators.CrossOver(self.fast_mv,self.slow_mv)
        # this crossover store 0 or 1 value if crossover happen it store 1 in crossunder happen it store -1
    def next(self):
        # this next check the codditon in each step
        # if posision is zero means no active trade there only that condition buy order will place
        if self.position.size == 0 :
            # self .crossover greter than one means which store zero or one value it means crossover happen
            if self.crossover >0 :
                # as per the above perams we are utilizing 0.95 money for trading but for safe side we should use only 0.50 % on money
                amount_to_invest = (self.params.order_percentage*self.broker.cash)
                # calcutaing the how much quntity we can purchase in that ammount
                self.size = math.floor(amount_to_invest/self.data.close)

                print("BUY {} SHARES OF {} AT {}".format(self.size , self.params.ticker , self.data.close[0]))
                # output of above print Sell 81 SHARES OF SPY AT 118.239998
                # BUY 87 SHARES OF SPY AT 110.0
                self.buy(size=self.size)
        if self.position.size > 0 :
            if self.crossover < 0 :
                print("Sell {} SHARES OF {} AT {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()


