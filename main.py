from ETF import *
from Stock import *


'''
~~~ ETF Analysis ~~~
Possibilities for columns:
'Ticker', 'Weighting'
'Sales Growth 3Y', 'Median Rev Growth 3Y'
'EBITDA Margin', 'Gross Margin', 'Operating Margin', 'Net Margin'
'EV/GP', 'EV/OP', 'Adj EV/OP', 'EV/EBITDA'
'GP/Employees'
'52W High'
'''

etf = ETF('mine')
# conditions = [['Operating Profit', '>', '5.00%']]
columns = ['Ticker', 'Sales Growth 3Y', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/OP', 'Gross Margin', 'Operating Margin', '52W High']

etf.display_metrics(columns)

"""
# Multiple ETF Analysis
#tickers = ['arkk', 'bulz', 'fngg', 'fngu', 'tecl', 'qqq', 'spy', 'vti']
#tickers = ['qqq', 'qld', 'tqqq']  # 1x, 2x, 3x comparison
#tickers = ['spy', 'sso', 'upro']  # 1x, 2x, 3x comparison
#tickers = ['iyw', 'rom', 'tecl']  # 1x, 2x, 3x comparison
#tickers = ['arkk', 'arkw', 'arkg', 'arkf', 'arkq', 'arkx']  # ARK invest ETFs
tickers = ['qqq', 'fngg', 'fngs', 'voo', 'vti', 'spy', 'rom', 'iyw']
for ticker in tickers:
    etf = ETF(ticker)
    print(ticker)
    #print(etf.holdings)
    print(etf.weighted_EV_to_EBITDA_ratio)
    print(etf.weighted_revenue_growth_3y)
    print()
"""
"""
# Multi stock analysis
#tickers = ['sq', 'shop', 'etsy', 'team', 'now', 'fb', 'amzn', 'crm', 'nvda', 'nflx', 'appf', 'googl', 'adbe', 'pypl', 'msft', 'aapl', 'ma', 'v']
#tickers = ['wmt', 'tgt', 'cost', 'hd', 'low', 'bby']  # Physical retail
tickers = ['aapl', 'msft', 'amzn', 'googl', 'fb', 'tsla', 'nflx', 'coin']  # Big Tech + some more
# Tickers are now callable as ticker objects
for ticker in tickers:
    stock = Stock(ticker)
    print(stock.name)
    print('EV/Revenue:', stock.ev_to_sales_ratio)
    print('EV/EBITDA:', stock.ev_to_ebitda_ratio)
    print('EBITDA past 3Y:', stock.ebitda_growth_3y)
    print('Sales past 3Y:', stock.revenue_growth_3y)
    print()
"""