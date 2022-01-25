from ETF import *
from Stock import *


'''
~~~ ETF Analysis ~~~
Possibilities for columns:
'Ticker', 'Weighting', 'Price', 'Market Cap', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income', 'CapEx'
'EV/GP', 'EV/EBITDA', 'EV/EBIT', 'Adj EV/EBIT'
'Sales Growth 3Y', 'Median Rev Growth 3Y'
'Gross Margin', 'EBITDA Margin', 'EBIT Margin', 'Net Margin'
'Beta', 'GP/Employees'
'52W High'
'''

etf = ETF('aapl msft googl amzn fb tsla nvda crm shop sq coin')
columns = ['Ticker', 'Market Cap', 'CapEx', 'Adj EV/EBIT', 'Median Rev Growth 3Y', 'Gross Margin', 'EBITDA Margin', 'EBIT Margin', '52W High']
etf.display_metrics(columns)

'''
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
'''
