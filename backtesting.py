from datetime import datetime
import backtrader as bt
import locale
from util import *
from krx_wr_script import *

locale.setlocale(locale.LC_ALL, 'ko_KR')

# Create a subclass of Strategy to define the indicators and logic
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        p_short=5,  # period for the fast moving average
        p_middle=20,  # period for the slow moving average
        p_long=100,
    )

    def __init__(self):
        ema1 = bt.ind.EMA(period=self.p.p_short)  # fast moving average
        ema2 = bt.ind.EMA(period=self.p.p_middle)  # slow moving average
        self.crossover = bt.ind.CrossOver(ema1, ema2)  # crossover signal
        self.rsi_14 = bt.ind.RSI_EMA(period=14)
        self.holding = 0

    def next(self):
        current_stock_price = self.data.close[0]

        if not self.position:  # not in the market
            if self.crossover < 0:  # if fast crosses slow to the upside
                available_stocks = self.broker.getcash() / current_stock_price
                self.buy(size=int((available_stocks) * 0.3))
            if self.rsi_14 < 20:
                # print(self.broker.getcash())
                available_stocks = self.broker.getcash() / current_stock_price
                self.buy(size=int((available_stocks) * 0.7))
        elif self.position:
            if self.crossover < 0:
                available_stocks = self.broker.getcash() / current_stock_price
                self.buy(size=int((available_stocks) * 0.2))
            if self.rsi_14 < 30:
                available_stocks = self.broker.getcash() / current_stock_price
                self.buy(size=int((available_stocks) * 0.15))
        # if self.rsi_14 < 10:
        #     # print(self.broker.getcash())
        #     available_stocks = self.broker.getcash() / current_stock_price
        #     self.buy(size=int((available_stocks) * 0.5))

        elif self.crossover > 0:  # in the market & cross to the downside
            available_stocks = self.broker.getcash() / current_stock_price
            if int((self.holding) * 0.15) > 0:
                self.sell(size=int((self.holding) * 0.5))
            else:
                self.close()
            # self.close()  # close long position
        if self.rsi_14 >= 70:
            available_stocks = self.broker.getcash() / current_stock_price
            if int((self.holding) * 0.15) > 0:
                self.sell(size=int((self.holding) * 0.25))
            else:
                self.close()

    def notify_order(self, order):
        if order.status not in [order.Completed]:
            return

        if order.isbuy():
            action = 'Buy'
        elif order.issell():
            action = 'Sell'

        stock_price = self.data.close[0]
        cash = self.broker.getcash()
        value = self.broker.getvalue()
        self.holding += order.size

        print('%s[%d] holding[%d] price[%d] cash[%.2f] value[%.2f]'
              % (action, abs(order.size), self.holding, stock_price, cash, value))


util_bt = util()
stock_name = '코리아센터'
stock_csv = pykrx_read_csv(stock_name, util_bt.Krx_Char_folder_path)
stock_csv['date'] = pd.to_datetime(stock_csv['date'])
stock_csv.set_index(stock_csv['date'], inplace=True)
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
cerebro.broker.setcash(1000000)
cerebro.broker.setcommission(0.002)


# Create a data feed
data = bt.feeds.PandasData(dataname=stock_csv)

cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy

start_value = cerebro.broker.getvalue()
cerebro.run()  # run it all
final_value = cerebro.broker.getvalue()

print('* start value : %s won' % locale.format_string('%d', start_value, grouping=True))
print('* final value : %s won' % locale.format_string('%d', final_value, grouping=True))
print('* earning rate : %.2f %%' % ((final_value - start_value)/ start_value * 100.0))

cerebro.plot()  # and plot it with a single command