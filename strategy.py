# vedio number 3
import backtrader as bt

# Create a Stratey


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in[order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log('BUY EXECUTED {}',format(order.executed.price))
                self.log('BUY EXECUTED, %.2f' % self.dataclose[0])
            elif order.issell() :
                # self.log('SELL EXECUTED {}', format(order.executed.price))
                self.log('SELL EXECUTED, %.2f' % self.dataclose[0])
            self.bar_executed = len(self)

        self.order = None


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        # print(len(self))
        # print(self.order) # this return order details
        # print(self.position) #this return position details
        if self.order:
            return
        if not self.position :
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()

        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL DONE, %.2f' % self.dataclose[0])
                self.order = self.sell()


        #we will sell the buy order after 5 candle
