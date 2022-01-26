from ETF import *
from Stock import *


'''
~~~ ETF Analysis ~~~
Possibilities for columns:
'Ticker', 'Weighting', 'Price', 'Market Cap', 'Enterprise Value', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income'
'EV/GP', 'EV/EBITDA', 'EV/EBIT', 'Adj EV/EBIT'
'Sales Growth 3Y', 'Median Rev Growth 3Y'
'Gross Margin', 'EBITDA Margin', 'EBIT Margin', 'Net Margin'
'Cash', 'Long Term Debt', 'Debt/EBIT', 'R&D', 'R&D/Revenue'
'Share Count Growth 3Y', 'Beta', 'GP/Employees'
'52W High'
'''

'''
stock = Stock('AAPL')
print(stock.cash)
exit(0)
'''

etf = ETF('aapl msft googl amzn fb tsla nvda crm adbe shop sq coin')
columns = ['Ticker', 'Market Cap', 'Enterprise Value', 'R&D', 'R&D/Revenue', 'Cash', 'Long Term Debt', 'Debt/EBIT', 'Share Count Growth 3Y', 'Adj EV/EBIT', 'Median Rev Growth 3Y', 'Gross Margin', 'EBITDA Margin', 'EBIT Margin', '52W High']
etf.display_metrics(columns, only_nums=True)

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
