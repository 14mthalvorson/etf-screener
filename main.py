# I just use this script to collect whatever data I need in the moment
# TODO: Investigate TSLA, VEEV, SE, WDAY, PINS

from Stock import *
from ETF import *


qqq = ETF('qqq')
print(qqq.holdings)
print(qqq.weighted_revenue_growth)



"""
tickers = ['sq', 'shop', 'etsy', 'team', 'now', 'fb', 'amzn', 'crm', 'nvda', 'nflx', 'appf', 'googl', 'adbe', 'pypl', 'msft', 'aapl', 'ma', 'v']


# Tickers are now callable as ticker objects

for ticker in tickers:
    stock = Stock(ticker)
    print(stock.name)
    print('EV/Revenue:', stock.ev_to_sales_ratio)
    print('EV/EBITDA:', stock.ev_to_ebitda_ratio)
    print('Sales past 3Y:', stock.revenue_growth_3y)
    print()
"""