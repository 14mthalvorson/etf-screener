# I just use this script to collect whatever data I need in the moment
# TODO: Investigate TSLA, VEEV, SE, WDAY, PINS

from Stock import *
from ETF import *


stock = Stock('tsla')
print(stock.revenue_growth_yoy)
print(stock.revenue_growth_3y)



"""
tickers = ['arkk', 'qqq', 'spy', 'vti']

for ticker in tickers:
    etf = ETF(ticker)
    print(ticker)
    print(etf.holdings)
    print(etf.weighted_EV_to_EBITDA_ratio)
    print()

"""
"""
tickers = ['sq', 'shop', 'etsy', 'team', 'now', 'fb', 'amzn', 'crm', 'nvda', 'nflx', 'appf', 'googl', 'adbe', 'pypl', 'msft', 'aapl', 'ma', 'v']


# Tickers are now callable as ticker objects

for ticker in tickers:
    stock = Stock(ticker)
    print(stock.name)
    #print('EV/Revenue:', stock.ev_to_sales_ratio)
    #print('EV/EBITDA:', stock.ev_to_ebitda_ratio)
    #print('Sales past 3Y:', stock.revenue_growth_3y)
    print('Revenue/Employee:', stock.revenue_per_employee)
    print()
    """
