# I just use this script to collect whatever data I need in the moment
# TODO: Investigate TSLA, VEEV, SE, WDAY, PINS

from Stock import *
from ETF import *




"""

tickers = ['arkk', 'qqq', 'spy', 'vti']

for ticker in tickers:
    etf = ETF(ticker)
    print(ticker)
    print(etf.holdings)
    print(etf.weighted_EV_to_EBITDA_ratio)
    print()


"""
#tickers = ['sq', 'shop', 'etsy', 'team', 'now', 'fb', 'amzn', 'crm', 'nvda', 'nflx', 'appf', 'googl', 'adbe', 'pypl', 'msft', 'aapl', 'ma', 'v']
#tickers = ['wmt', 'tgt', 'cost', 'hd', 'low', 'bby']  # Physical retail
tickers = ['aapl', 'msft', 'amzn', 'googl', 'fb']  # Big Tech

# Tickers are now callable as ticker objects

for ticker in tickers:
    stock = Stock(ticker)
    print(stock.name)
    print('EV/Revenue:', stock.ev_to_sales_ratio)
    print('EV/EBITDA:', stock.ev_to_ebitda_ratio)
    print('EBITDA past 3Y:', stock.ebitda_growth_3y)
    print('Sales past 3Y:', stock.revenue_growth_3y)
    print('Revenue/Employee:', stock.revenue_per_employee)
    print('EBITDA/Employee:', stock.ebitda_per_employee)
    print()

