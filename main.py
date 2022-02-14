from ETF import ETF
from Stock import Stock
from Crypto import Crypto
from cache import *


''' Options for "columns" list below:

ETF Growth Metrics:
'Adj Rev Growth 3Y', 'Leveraged Rev Growth 3Y'
'Median TTM Rev Growth 3Y', 'Median Q/Q Rev Growth 3Y', 'Annualized Rev Growth 3Y'
'% >7% Rev Growth'
'1 Year Return', '3 Year Return', '5 Year Return', '10 Year Return'

ETF Valuation Metrics:
'EV/GP', 'Adj EV/EBIT', 'EV/EBIT'

ETF Health Metrics:
'% Pos Rev Growth', '% Pos EBIT Margin', '% at 52W High', '% at 52W Low'
'52W High', 'SMA20', 'SMA50', 'SMA200'

Other ETF Metrics:
'Ticker', 'Name', 'Type', 'Num Holdings', 'Weight', 'Price'
'Gross Margin', 'Adj EBIT Margin'
'Price to FVE'
'Leverage', 'Expense Ratio'

Stock Metrics:
'Ticker', 'Type', 'Weight', 'Price', 'Market Cap', 'Enterprise Value', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income'
'EV/GP', 'EV/EBITDA', 'Adj EV/EBIT', 'EV/EBIT'
'Adj Rev Growth 3Y', 'Median TTM Rev Growth 3Y', 'Median Q/Q Rev Growth 3Y', 'Annualized Rev Growth 3Y', 'Median Rev Growth'
'Gross Margin', 'EBITDA Margin', 'Adj EBIT Margin', 'EBIT Margin', 'Net Margin'
'Cash', 'Long Term Debt', 'Debt/EBIT', 'Debt/GP', 'R&D', 'R&D/Revenue'
'Share Count Growth 3Y', 'Beta', 'GP/Employees', 'Dividend %'
'SMA20', 'SMA50', 'SMA200', '52W High'
'Morningstar FVE', 'Price to FVE'
'Price to FVE'

Crypto:
'Ticker', 'Name', 'Type', 'Weight', 'Price'
'''


etf = ETF('all')
columns = ['Ticker', 'Name', 'Weight', 'Type', 'Num Holdings', 'Leverage', 'Expense Ratio', 'Martin Score', 'Adj Rev Growth 3Y', '1 Year Return', '3 Year Return', '5 Year Return', '10 Year Return', 'Volatility']
etf.display_metrics(columns, only_nums=True, extra_header=False, include_overall=True)

exit(0)

etf = ETF('webl')
columns = ['Ticker', 'Name', 'Weight', 'Type', 'Num Holdings', 'Leverage', 'Expense Ratio', 'Martin Score', 'Adj Rev Growth 3Y', 'Leveraged Rev Growth 3Y', 'Gross Margin', 'Adj EBIT Margin', 'EV/GP', 'Adj EV/EBIT', 'Debt/GP', 'Perf Year', '52W High', 'SMA20', 'SMA200', 'Volatility', '% Pos Rev Growth', '% >7% Rev Growth', '% Pos EBIT Margin', '% at 52W High', '% at 52W Low']
etf.display_metrics(columns, only_nums=True, extra_header=False, include_overall=True)


