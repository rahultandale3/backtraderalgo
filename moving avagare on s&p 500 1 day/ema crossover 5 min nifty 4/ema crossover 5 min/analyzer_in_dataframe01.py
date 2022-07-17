import datetime
import backtrader as bt
import pandas as pd

class BarAnalysis(bt.analyzers.Analyzer):

    def start(self):
        self.rets = list()

    def next(self):

        try:
            self.rets.append(
                [
                    self.datas[0].datetime.datetime(),
                    self.datas[0].open[0],
                    # self.datas[0].high[0],
                    # self.datas[0].low[0],
                    self.datas[0].close[0],
                    # self.datas[0].volume[0],
                    self.strategy.getposition().size,
                    self.strategy.broker.getvalue(),
                    self.strategy.broker.getcash(),
                ]
            )
        except:
            pass

    def get_analysis(self):
        return self.rets
