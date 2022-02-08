from ETF import ETF
from Stock import Stock
from Crypto import Crypto


'''
Both Stock & ETF Columns:
'Ticker', 'Name', 'Type', 'Weight', 'Price'
'EV/GP', 'Adj EV/EBIT', 'EV/EBIT'
'Adj Rev Growth 3Y', 'Median TTM Rev Growth 3Y', 'Median Q/Q Rev Growth 3Y', 'Annualized Rev Growth 3Y'
'Gross Margin', 'Adj EBIT Margin'
'52W High', 'SMA20', 'SMA50', 'SMA200'
'Price to FVE'

Stock Columns:
'Ticker', 'Type', 'Weight', 'Price', 'Market Cap', 'Enterprise Value', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income'
'EV/GP', 'EV/EBITDA', 'Adj EV/EBIT', 'EV/EBIT'
'Adj Rev Growth 3Y', 'Median TTM Rev Growth 3Y', 'Median Q/Q Rev Growth 3Y', 'Annualized Rev Growth 3Y', 'Median Rev Growth'
'Gross Margin', 'EBITDA Margin', 'Adj EBIT Margin', 'EBIT Margin', 'Net Margin'
'Cash', 'Long Term Debt', 'Debt/EBIT', 'Debt/GP', 'R&D', 'R&D/Revenue'
'Share Count Growth 3Y', 'Beta', 'GP/Employees', 'Dividend %'
'Perf Year', 'SMA20', 'SMA50', 'SMA200', '52W High'
'Morningstar FVE', 'Price to FVE'

ETF Columns:
'Weighted Median EV/GP', 'Weighted Median Adj EV/EBIT', 'Weighted Median EV/EBIT'
'Weighted Median Median Rev Growth 3Y'
'Weighted Median Gross Margin', 'Weighted Median Adj EBIT Margin'
'% at 52W High', '% at 52W Low'
'Leverage'
'Price to FVE'

Crypto:
'Ticker', 'Name', 'Type', 'Weight', 'Price'
'''


etf = ETF('vym vong vonv')
# columns = ['Ticker', 'Price to FVE']
columns = ['Ticker', 'Name', 'Type', 'Leverage', 'Adj Rev Growth 3Y', 'Gross Margin', 'Adj EBIT Margin', 'EV/GP', 'Adj EV/EBIT', 'Debt/GP', 'Perf Year', '52W High', 'SMA20', 'SMA200', '% at 52W High', '% at 52W Low']
etf.display_metrics(columns, only_nums=True, extra_header=False, include_overall=True)
