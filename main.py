from ETF import *
from Stock import *


'''
~~~ ETF Analysis ~~~
Possibilities for columns:
'Ticker', 'Weighting'
'Sales Growth 3Y', 'Median Rev Growth 3Y'
'EBITDA Margin', 'Gross Margin', 'Operating Margin', 'Net Margin'
'EV/GP', 'EV/OP', 'Adj EV/OP', 'EV/EBITDA', 'Potential EV/OP'
'GP/Employees'
'52W High'
'''


etf = ETF('op')
# conditions = [['Operating Profit', '>', '5.00%'], ['Years Public', '>=', '1.0']]
# columns = ['Ticker', '52W High']
# columns = ['Ticker', 'Sales Growth 3Y', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/OP', 'Gross Margin', 'Operating Margin', '52W High']
columns = ['Ticker', 'Median Rev Growth 3Y', 'Potential EV/OP', 'Adj EV/OP', 'Operating Margin', '52W High']

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
